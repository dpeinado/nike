 #-*- coding: utf-8 -*-

from django.db import models
from datetime import datetime, date, timedelta
from django.core.exceptions import ObjectDoesNotExist
from core.utility import alldaysinyear
import csv
from operator import itemgetter

from guardias.exceptions import NoExisteCalendario, ConsistenciaCalendario, ExisteCalendario

class guardiasManager(models.Manager):

    def check_existencia(self, year):
        """
        Compruebo si existe el calendario.
        :param year:
        :return: True si existe, False si no
        """
        try:
            primerdia = datetime(year, 1, 1).toordinal()
            guardia1 = self.get(pk=primerdia)
            return True
        except ObjectDoesNotExist:
            return False

    def check_consistencia(self, year):
        """
        Veo la consistencia del calendario. Tiene que haber el correcto número de días, y tienen que ser
        consecutivos. Si falla alguna condición se arroja una excepción que tiene que ser capturada
        aguas arriba
        :param year:
        :return:
        """
        if self.check_existencia(year):
            inicio = datetime(year, 1, 1).toordinal()
            finaño = datetime(year, 12, 31).toordinal()
            misdias = super(guardiasManager, self).get_queryset().filter(id__gte=inicio, id__lte=finaño)
            if (finaño-inicio+1) != len(misdias):
                raise ConsistenciaCalendario(
                    "Error: intervalo entre final y principio de año no coincide con días devueltos")
            for guardia in misdias:
                self.check_fecha(guardia)
        else:
            raise NoExisteCalendario("El calendario para el año {} no existe".format(year))

    def check_fecha(self, dia):
        """
        una de las comprobaciones de consistencia del calendario. El id tiene que ser el ordinal de fecha.
        Si falla arroja una excepción.
        :param dia:
        :return:
        """
        if dia.fecha.toordinal() != dia.id:
            raise ConsistenciaCalendario(
                "Error: guardia con fecha no coincidente con el ordinal"
            )

    def set_allSundaysSaturdays(self, year):
        """
        Coloco todos los domingos a sábados en primera instancia
        :param year:
        :return:
        """
        for d in alldaysinyear(year, 6):
            g = self.get(pk=d.toordinal())
            g.tipo = self.model.FES_FES
            g.save()

    def set_allSaturdays (self, year):
        """
        Coloco todos los sábados a sábado en primera instancia
        :param year:
        :return:
        """
        for d in alldaysinyear(year, 5):
            g = self.get(pk=d.toordinal())
            g.tipo = self.model.FES_FES
            g.save()

    def crea_calendario(self, year):
        """
        Si no existe, creo el calendario dado por year. Si existe arrojo una excepción
        para que se atrape aguas arriba
        :param year:
        :return:
        """
        if not self.check_existencia(year):
            inicio = datetime(year, 1, 1).toordinal()
            finaño = datetime(year, 12, 31).toordinal()
            for anio in range(inicio, finaño+1):
                self.create(
                    fecha = datetime.fromordinal(anio)
                )
        else:
            raise ExisteCalendario("El calendario para el año {} ya existe".format(year))

    def set_FES_LAB(self, year):
        """
        Para todos los festivos, detecto cuales tienen después laborable
        (LAB_LAB o LAB_FES, ya que los LAB_LAB_FES todavía no están puestos), y
        los coloco como domingos (FES_LAB)
        :param year:
        :return:
        """
        festivos = self.filter(tipo=self.model.FES_FES).order_by('id')
        for dia in festivos:
            try:
                siguiente = self.get(pk=dia.pk+1)
            except ObjectDoesNotExist:
                continue
            if siguiente.tipo == self.model.LAB_LAB or siguiente.tipo == self.model.LAB_FES:
                dia.tipo = self.model.FES_LAB # ESTE DÍA ES TIPO SÁBADO
                dia.save()

    def set_LAB_FES(self, year):
        """
        Busco los viernes (laborable (LAB_LAB) que estén antes de un Festivo (FES_FES o FES_LAB), ya
        que pueden ser días antes de festivo (FES_LAB)
        :param year:
        :return:
        """
        laborables = self.filter(tipo=self.model.LAB_LAB).order_by('id')
        for dia in laborables:
            try:
                siguiente = self.get(pk=dia.pk+1)
            except ObjectDoesNotExist as e:
                continue
            if siguiente.tipo == self.model.FES_FES or siguiente.tipo == self.model.FES_LAB:
                dia.tipo = self.model.LAB_FES
                dia.save()

    def set_LAB_LAB_FES(self, year):
        laborables = self.filter(tipo=self.model.LAB_LAB).order_by('id')
        for dia in laborables:
            try:
                siguiente = self.get(pk=dia.pk+1)
            except ObjectDoesNotExist:
                continue
            if siguiente.tipo == self.model.LAB_FES:
                dia.tipo = self.model.LAB_LAB_FES
                dia.save()

    def set_calendario(self, year, fichero):
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
        :param year:
        :param fichero:
        :return:
        """

        # 1
        try:
            self.crea_calendario(year)
            print('OK: Calendario creado para el año {}'.format(year))
        except ExisteCalendario:
            print("""
                Error: este año ({}) ya se encuentra en la base de datos.
                Borre primero el año""".format(year))
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
                g = self.get(pk=festivo)
                g.tipo = self.model.FES_LAB
                g.save()
        print('OK: Añadidos los festivos para el año {}'.format(year))
        # 3
        self.set_allSundaysSaturdays(year) # Domingos FES_FES
        print('OK: Domingos como sábados para el año {}'.format(year))
        # 4
        self.set_allSaturdays(year) # Sábados FES_FES
        print('OK: Sábados para el año {}'.format(year))

        # 5
        self.set_FES_LAB(year)

        #6
        self.set_LAB_FES(year)

        # 7
        self.set_LAB_LAB_FES(year)

    def get_dias_tipo_year(self, year, ptipo):
        dias = self.filter(tipo=ptipo).order_by('pk')
        return dias

    def get_calendario(self, year):
        micalendario = []

        mtipo = self.model.LAB_LAB
        respuesta = self.get_dias_tipo_year(year, mtipo)
        micalendario.append([len(respuesta), respuesta])

        mtipo = self.model.LAB_LAB_FES
        respuesta = self.get_dias_tipo_year(2015, mtipo)
        micalendario.append([len(respuesta), respuesta])

        mtipo = self.model.LAB_FES
        respuesta = self.get_dias_tipo_year(2015, mtipo)
        micalendario.append([len(respuesta), respuesta])

        mtipo = self.model.FES_FES
        respuesta = self.get_dias_tipo_year(2015, mtipo)
        micalendario.append([len(respuesta), respuesta])

        mtipo = self.model.FES_LAB
        respuesta = self.get_dias_tipo_year(2015, mtipo)
        micalendario.append([len(respuesta), respuesta])

        return sorted(micalendario, key=itemgetter(0))

    def get_num_festivos(self, comienzo, final):
        return len(
            self.filter(
                pk__gte=comienzo.toordinal()
            ).filter(
                pk__lte=final.toordinal()
            ).filter(tipo__gte=3))
