Useful SQLs
***********
`Data Source`_

Найти те фразы, у которых отличается модуль в английском и русском переводе
===========================================================================

.. code:: sql

   SELECT eng_phrase.Phrase, eng_phrase.Translation, eng_phrase.Module, rus_phrase.Translation, rus_phrase.Module
   FROM int_Phrase eng_phrase
   LEFT JOIN int_Phrase rus_phrase ON eng_phrase.Phrase = rus_phrase.Phrase AND rus_phrase.LanguageId = 2
   WHERE (eng_phrase.LanguageId = 1) AND (eng_phrase.Module <> rus_phrase.Module)

Поставить всем пользователям в базе тестовые почтовые адреса (с возможностью обращения процесса)
================================================================================================

.. code:: sql

   UPDATE int_PortalUser
   SET Email = CONCAT(REPLACE(Email, '@', '_at_'), '@alex.in-portal.net')
   WHERE Email <> ''

Массово поменять основную (primary) группу пользователям
========================================================

.. code:: sql

   UPDATE `int_UserGroup`
   SET GroupId = 20
   WHERE (GroupId = 13) AND (PrimaryGroup = 1) AND (PortalUserId BETWEEN 1600 AND 2100)

Заменить Email пользователям из перечисленных групп (используется sub-select query)
===================================================================================

.. code:: sql

   UPDATE int_PortalUser
   SET Email = REPLACE(Email, '@alex.in-portal.net', '@osaka.intechnic.com')
   WHERE PortalUserId IN (
       SELECT PortalUserId
       FROM int_UserGroup
       WHERE PrimaryGroup = 1 AND (GroupId IN (19,20))
   )

Найти названия переменных, у которых есть дубликаты в таблице PersistentSessionData
===================================================================================

.. code:: sql

   SELECT PortalUserId, VariableName, COUNT(*)
   FROM `int_PersistantSessionData`
   GROUP BY PortalUserId, VariableName
   HAVING COUNT(*) > 1
   ORDER BY `PortalUserId` ASC , `VariableName` ASC

Убрать компонент даты из временной метки (timestamp)
====================================================

.. code:: sql

   UPDATE int_Flights
   SET DepartureTime = UNIX_TIMESTAMP(
           CONCAT(
               MAKEDATE(
                   1970,
                   1
               ),
               ' ',
               MAKETIME(
                   DATE_FORMAT(FROM_UNIXTIME(DepartureTime), '%H'),
                   DATE_FORMAT(FROM_UNIXTIME(DepartureTime), '%i'),
                   DATE_FORMAT(FROM_UNIXTIME(DepartureTime), '%s')
               )
           )
       )
   WHERE DepartureTime > 75599;

Изменить пароль у "root" пользователя
=====================================

.. code:: sql

   UPDATE `int_ConfigurationValues`
   SET VariableValue = MD5( CONCAT(MD5('root'), 'b38') )
   WHERE VariableName = 'RootPass';

   TRUNCATE TABLE int_Cache;

.. note::

   Во всех SQL запросах (в данной статье) ``int_`` это :ref:`const_TABLE_PREFIX`.

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:Useful_SQLs
