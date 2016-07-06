 #-*- coding: utf-8 -*-

from django.db import models
from datetime import datetime, date, timedelta
import locale
import collections

import calendar
from django.core.exceptions import ObjectDoesNotExist
from core.utility import alldaysinyear
import csv
from operator import itemgetter
from nike.users.models import User

from guardias.exceptions import NoExisteCalendario
from guardias.exceptions import ConsistenciaCalendario
from guardias.exceptions import ExisteCalendario
from guardias.exceptions import IllegalArgumentError
from guardias.exceptions import ProgramAllYearDone

class guardiasManager(models.Manager):

    def check_existencia(self, year, centro_id):
        """
        Compruebo si existe el calendario.
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return: True si existe, False si no
        """
        try:
            primerdia = datetime(year, 1, 1).toordinal()
            guardia1 = self.get(fecha=primerdia, centro=centro_id)
            return True
        except ObjectDoesNotExist:
            return False

    def check_consistencia(self, year, centro_id):
        """
        Veo la consistencia del calendario. Tiene que haber el correcto número de días, y tienen que ser
        consecutivos. Si falla alguna condición se arroja una excepción que tiene que ser capturada
        aguas arriba
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        if self.check_existencia(year, centro_id):
            inicio = datetime(year, 1, 1).toordinal()
            finaño = datetime(year, 12, 31).toordinal()
            misdias = self.filter(fecha__gte=inicio, fecha__lte=finaño, centro=centro_id)
            if (finaño-inicio+1) != len(misdias):
                raise ConsistenciaCalendario(
                    "Error: intervalo entre final y principio de año no coincide con días devueltos")
            # for guardia in misdias:
            #     self.check_fecha(guardia)
        else:
            raise NoExisteCalendario("El calendario para el año {} no existe".format(year))

    # def check_fecha(self, dia):
    #     """
    #     una de las comprobaciones de consistencia del calendario. El id tiene que ser el ordinal de fecha.
    #     Si falla arroja una excepción.
    #     :param dia:
    #     :return:
    #     """
    #     if dia.fecha.toordinal() != dia.id:
    #         raise ConsistenciaCalendario(
    #             "Error: guardia con fecha no coincidente con el ordinal"
    #         )

    def set_allSundaysSaturdays(self, year, centro_id):
        """
        Coloco todos los domingos a sábados en primera instancia
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        for d in alldaysinyear(year, 6):
            g = self.get(fecha=d.toordinal(), centro=centro_id)
            g.tipo = self.model.FES_FES
            g.save()

    def set_allSaturdays (self, year, centro_id):
        """
        Coloco todos los sábados a sábado en primera instancia
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        for d in alldaysinyear(year, 5):
            g = self.get(fecha=d.toordinal(), centro=centro_id)
            g.tipo = self.model.FES_FES
            g.save()

    def crea_calendario(self, year, centro_id):
        """
        Si no existe, creo el calendario dado por year. Si existe arrojo una excepción
        para que se atrape aguas arriba
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        from .models import Centro
        if not self.check_existencia(year, centro_id):
            inicio = datetime(year, 1, 1).toordinal()
            finaño = datetime(year, 12, 31).toordinal()
            micentro = Centro.objects.get(pk=centro_id)
            for dia in range(inicio, finaño+1):
                try:
                    self.create(fecha = dia,centro=micentro)
                except Exception as e:
                    pass
        else:
            raise ExisteCalendario("El calendario para el año {} ya existe".format(year))

    def set_FES_LAB(self, year, centro_id):
        """
        Para todos los festivos, detecto cuales tienen después laborable
        (LAB_LAB o LAB_FES, ya que los LAB_LAB_FES todavía no están puestos), y
        los coloco como domingos (FES_LAB)
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        festivos = self.filter(tipo=self.model.FES_FES, centro=centro_id).order_by('fecha')
        for dia in festivos:
            try:
                siguiente = self.get(fecha=dia.fecha+1, centro=centro_id)
            except ObjectDoesNotExist:
                continue
            if siguiente.tipo == self.model.LAB_LAB or siguiente.tipo == self.model.LAB_FES:
                dia.tipo = self.model.FES_LAB # ESTE DÍA ES TIPO SÁBADO
                dia.save()

    def set_LAB_FES(self, year, centro_id):
        """
        Busco los viernes (laborable (LAB_LAB) que estén antes de un Festivo (FES_FES o FES_LAB), ya
        que pueden ser días antes de festivo (FES_LAB)
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        laborables = self.filter(tipo=self.model.LAB_LAB, centro_id=centro_id).order_by('fecha')
        for dia in laborables:
            try:
                siguiente = self.get(fecha=dia.fecha+1, centro_id=centro_id)
            except ObjectDoesNotExist as e:
                continue
            if siguiente.tipo == self.model.FES_FES or siguiente.tipo == self.model.FES_LAB:
                dia.tipo = self.model.LAB_FES
                dia.save()

    def set_LAB_LAB_FES(self, year, centro_id):
        """
        Se buscan los días lab_lab, cuyo día siguiente es un lab_fes. Es decir,
        buscamos los jueves.
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        laborables = self.filter(tipo=self.model.LAB_LAB, centro_id=centro_id).order_by('fecha')
        for dia in laborables:
            try:
                siguiente = self.get(fecha=dia.fecha+1, centro_id=centro_id)
            except ObjectDoesNotExist:
                continue
            if siguiente.tipo == self.model.LAB_FES:
                dia.tipo = self.model.LAB_LAB_FES
                dia.save()

    def set_calendario(self, year, fichero, centro_id):
        """
        Secuencia para la creación del calendario. Está dividida en
        varias fases:
            1.- Creo el calendario. Si existe calendario para ese año
                Error, y no se crea (mensaje diciendo que se borre)
            2.- Lectura del fichero de festivos. Formato 2015-01-01
            3.- Se colocan los domingos como sábados
            4.- se colocan los sábados
            5.- busco los festivos y los que luego tengan laborable
                (LAB_LAB o LAB_FES) (laborable o viernes), les coloco
                el FES_LAB
            6.- Busco los tipo viernes o antes de puente LAB_FES
            7.- Busco los tipo jueves, o laborable antes de uno tipo 6
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :param fichero: fichero de festivos
        :return:
        """

        # 1
        try:
            self.crea_calendario(year, centro_id)
            # print('OK: Calendario creado para el año {}'.format(year))
        except ExisteCalendario:
            # print("""
            #     Error: este año ({}) ya se encuentra en la base de datos.
            #     Borre primero el año""".format(year))
            raise ExisteCalendario()
            return

        # 2
        with open(fichero, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                festivo = datetime.strptime(row[0], "%Y-%m-%d").date()
                if festivo.year != year:
                    print("Festivo en el fichero no es del año {}".format(year))
                festivo=festivo.toordinal()
                g = self.get(fecha=festivo, centro_id=centro_id)
                g.tipo = self.model.FES_LAB
                g.save()
        # print('OK: Añadidos los festivos para el año {}'.format(year))
        # 3
        self.set_allSundaysSaturdays(year, centro_id) # Domingos FES_FES
        # print('OK: Domingos como sábados para el año {}'.format(year))
        # 4
        self.set_allSaturdays(year, centro_id) # Sábados FES_FES
        # print('OK: Sábados para el año {}'.format(year))

        # 5
        self.set_FES_LAB(year, centro_id)

        #6
        self.set_LAB_FES(year, centro_id)

        # 7
        self.set_LAB_LAB_FES(year, centro_id)

    def get_dias_tipo_intervalo(self, inicio, fin, ptipo, centro_id):
        dias = self.filter(
            fecha__gte=inicio.toordinal(), fecha__lte=fin.toordinal(),
            tipo=ptipo, centro=centro_id).order_by('fecha')
        return dias

    def get_dias_tipo_year(self, year, ptipo, centro_id):
        """
        Proporciona el número los días de un cierto tipo
        en el calendario de guardias. Por ejemplo,
        get_dias_tipo_year(2015, Guardias.LAB_LAB) proporciona
        todos los laborables seguidos de laborable del año 2015
        :param year: Año del calendario
        :param ptipo: tipo de guardia
        :param centro_id: Centro al que pertenece el calendario
        :return: una query de Guardia
        """
        inicio=date(year,1,1).toordinal()
        fin=date(year,12,31).toordinal()
        dias = self.filter(
            fecha__gte=inicio, fecha__lte=fin,
            tipo=ptipo, centro=centro_id).order_by('fecha')
        return dias

    def get_calendario_intervalo(self, inicio, fin, centro_id):
        micalendario = []
        mitipo = self.model.LAB_LAB
        for mitipo, desc in self.model.TIPOS_GUARDIA:
            respuesta = self.get_dias_tipo_intervalo(inicio, fin, mitipo, centro_id=centro_id)
            micalendario.append([len(respuesta), mitipo, respuesta])

        return sorted(micalendario, key=itemgetter(0), reverse=True)


    def get_calendario(self, year, centro_id):
        """
        Proporciona una lista de listas [número días, tipo de día, query de días].
        Esta lista está ordenada según el número de días de forma ascendente. La
        primera lista corresponde al tipo de guardia del que hay menos en el año, y
        por tanto más rígido a la hora de programar.
        El propósito de esta función es proporcionar en orden las guardias que hay que
        asignar, primero las de las que hay menos, y finalmente de las que hay más.
        ************
        Esto último no lo tengo claro. Quizá esto añada demasiada rigidez. Quizá es más
        fácil empezar con los que hay más (lab_lab), y acabar con los que hay menos
        ************
        :param year: Año del calendario de guardias
        :param centro_id: Centro al que pertenece el calendario
        :return:
        """
        micalendario = []

        mtipo = self.model.LAB_LAB
        respuesta = self.get_dias_tipo_year(year, mtipo, centro_id=centro_id)
        micalendario.append([len(respuesta), mtipo, respuesta])

        mtipo = self.model.LAB_LAB_FES
        respuesta = self.get_dias_tipo_year(year, mtipo, centro_id=centro_id)
        micalendario.append([len(respuesta), mtipo, respuesta])

        mtipo = self.model.LAB_FES
        respuesta = self.get_dias_tipo_year(year, mtipo, centro_id=centro_id)
        micalendario.append([len(respuesta), mtipo, respuesta])

        mtipo = self.model.FES_FES
        respuesta = self.get_dias_tipo_year(year, mtipo, centro_id=centro_id)
        micalendario.append([len(respuesta), mtipo, respuesta])

        mtipo = self.model.FES_LAB
        respuesta = self.get_dias_tipo_year(year, mtipo, centro_id=centro_id)
        micalendario.append([len(respuesta), mtipo, respuesta])

        return sorted(micalendario, key=itemgetter(0), reverse=True)

    def get_num_festivos(self, comienzo, final, centro_id):
        """
        Proporciona el número de festivos entre dos fechas
        :param comienzo:
        :param final:
        :return:
        """
        if not isinstance(comienzo, date) or not isinstance(final, date):
            raise IllegalArgumentError("Error en los argumentos a get_num_festivos")
        return len(
            self.filter(
                fecha__gte=comienzo.toordinal()
            ).filter(
                fecha__lte=final.toordinal()
            ).filter(tipo__gte=3
            ).filter(centro_id=centro_id)
        )

    def set_vacaciones(self, rangodias, persona):
        """
        Coloca en el calendario de guardias para la persona dada los días marcados en la
        lista rango dias como ausencias previstas (vacaciones o días de otro tipo).
        :param rangodias: lista con dates para todos los días. Si quieres incluir un rango, hacerlo antes de
         la llamada a la función
        :param persona: Persona a la cual se van a colocar las ausencias.
        :return: Nothing
        """
        correcto = False
        if isinstance(rangodias, list): # and isinstance(persona, User):
            if all(isinstance(n, date) for n in rangodias):
                correcto = True

        if correcto:
            for dia in rangodias:
                miguardia = self.get(fecha=dia.toordinal())
                miguardia.ausencias.add(persona)
                miguardia.save()

        else:
            raise IllegalArgumentError("Error en los argumentos a set_vacaciones")

    def num_guardias_tipo_asignadas(self, quien, hoy, tipo):
        if not isinstance(quien, User):
            raise IllegalArgumentError("Error en los argumentos a num_guardias_tipo_asignadas")
        añocorriente = date.fromordinal(hoy).year
        inicio = date(añocorriente, 1, 1).toordinal()
        return self.filter(
            owner = quien
        ).filter(
            fecha__gte=inicio
        ).filter(
            fecha__lte=hoy
        ).filter(
            tipo=tipo
        ).count()

    def get_all_shifts_year(self, año, centro_id):
        return self.filter(
            fecha__gte=date(año,1,1).toordinal()
        ).filter(
            fecha__lte=date(año,12,31).toordinal()
        ).filter(centro_id=centro_id)

    def check_shift_between_free_days(self, miguardia, person, d1, d2):
        if miguardia.fecha == d1:
            siguiente = self.get(fecha=miguardia.fecha+1, centro=miguardia.centro)
            if siguiente.owner == person:
                return False
        elif miguardia.fecha == d2:
            anterior = self.get(fecha=miguardia.fecha-1, centro=miguardia.centro)
            if anterior.owner == person:
                return False
        else:
            siguiente = self.get(fecha=miguardia.fecha+1, centro=miguardia.centro)
            anterior  = self.get(fecha=miguardia.fecha-1, centro=miguardia.centro)
            if siguiente.owner == person or anterior.owner == person:
                return False
        if person in miguardia.ausencias.all():
            return False
        return True

    def clear_ausencias_intervalo(self, inicio, fin, centro_id):
        micalendario = self.get_calendario_intervalo(inicio, fin, centro_id)
        respuesta = {}
        for cuantas, tipo, guardias in micalendario:
            libres = []
            for g in guardias:
                if g.owner in g.ausencias:
                    g.owner = None
                    g.save()
                    libres.append(g)
            respuesta[tipo] = libres
        return respuesta

    def program_shifts_interval(self, inicio, fin, centro_id):
        from .models import ListaGuardias
        #micalendario = self.get_calendario_intervalo(inicio, fin, centro_id)
        libres = self.clear_ausencias_intervalo(inicio, fin, centro_id)
        for tipo in libres.keys():
            for g in libres[tipo]:
                lista = ListaGuardias.objects.get_lista(centro_id, tipo)
                for elem in lista.order_by('orden'):
                    p = User.objects.get(username=elem.user)
                    if self.check_shift_between_free_days(g, p, inicio.toordinal(), fin.toordinal()):
                        g.owner = p
                        ListaGuardias.objects.elem_to_bottom(centro_id, tipo, elem.orden)
                        break
                    else:
                        pass
                g.save()

    def program_shifts_all_year(self, year, centro_id):
        from .models import ListaGuardias
        micalendario = self.get_calendario(year, centro_id)
        day1 = date(year,1,1).toordinal()
        day2 = date(year,12,31).toordinal()
        for cuantas, tipo, guardias in micalendario:
            for g in guardias:
                if g.owner:
                    raise ProgramAllYearDone("Ya se ha programado el año entero")
                # lista = ListaGuardias.objects.get_lista(centro_id, tipo)
                # cual = 0
                # for elem in lista.order_by('orden'):
                #     p = User.objects.get(username=elem.user)
                #     if self.check_shift_between_free_days(g, p, day1, day2):
                #         g.owner = p
                #         ListaGuardias.objects.elem_to_bottom(centro_id, tipo, elem.orden)
                #         break
                #     else:
                #         pass
                # g.save()
                lista = User.guardias.get_next_user_tipo(tipo, g.fecha, g.centro, 5)
                cual = 0
                while cual < len(lista):
                    p = lista[cual][4]
                    if self.check_shift_between_free_days(g, p, day1, day2):
                        g.owner = p
                        break
                    else:
                        cual+=1
                g.save()


    def cuantas_guardias_mes(self, year, centro_id):
        usuarios = User.objects.filter(centro_id=centro_id)
        respdict = {}
        for usuario in usuarios:
            userdict = {}
            for mes in range(1,13):
                inicio = date(year, mes, 1)
                locale.setlocale(locale.LC_ALL, "es_ES")
                nombremes = inicio.strftime("%b")
                locale.setlocale(locale.LC_ALL, locale.getdefaultlocale()[0])
                inicio = inicio.toordinal()
                fin = date(year, mes, calendar.monthrange(year, mes)[1]).toordinal()
                respuesta = []
                total = 0
                for tipo, descripcion in self.model.TIPOS_GUARDIA:
                    cuantas = self.filter(
                            fecha__gte=inicio,
                            fecha__lte=fin,
                            owner=usuario,
                            tipo=tipo
                        ).count()
                    respuesta.append(cuantas)
                    total += cuantas
                respuesta.append(total)
                userdict[nombremes] = respuesta
            respdict[usuario.username] = userdict
        return respdict


class listaGuardiasManager(models.Manager):
    def get_lista(self, centro, tipo):
        return self.get_queryset().filter(centro=centro,tipo=tipo)

    def elem_to_bottom(self, centro, tipo, elemorden):
        lista = self.get_queryset().filter(
            centro=centro,
            tipo=tipo).order_by('orden')
        tobottom = lista.get(orden=elemorden)
        tobottom.orden=999
        tobottom.save()
        for elem in lista.order_by('orden'):
            if elem.orden>elemorden:
                elem.orden-=1
                elem.save()
        tobottom.orden = len(lista)
        tobottom.save()

    def shift_n(self, centro, tipo, n):
        for i in range(0,n):
            self.elem_to_bottom(centro,tipo,1)
