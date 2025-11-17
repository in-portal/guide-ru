OnAfterCopyToLive
=================
`Data Source`_

Данное событие вызывается для каждой записи после её копирования из
:doc:`временной таблицы </database/using_temporary_tables>` в оригинальную.

Вызывается из событий
---------------------

Данное событие косвенно (через метод ``kTempTablesHandler::DoCopyTempToOriginal``) вызывается из
события :doc:`/events/temp_editing/on_save` в процессе копирования данных из
:doc:`временной таблицы </database/using_temporary_tables>` в оригинальную.

Входные параметры
-----------------

+---------------------------------------+---------------------------------------------------------------------+
| название                              | описание                                                            |
+=======================================+=====================================================================+
| .. config-property::                  | ``ID``, которое получила запись после её копирования из             |
|    :name: id                          | :doc:`временной таблицы </database/using_temporary_tables>`         |
|    :type: int                         | в оригинальную.                                                     |
|    :ref_prefix: ep_OnAfterCopyToLive_ |                                                                     |
+---------------------------------------+---------------------------------------------------------------------+
| .. config-property::                  | ``ID``, которое было у записи во                                    |
|    :name: temp_id                     | :doc:`временной таблице </database/using_temporary_tables>`.        |
|    :type: int                         | Данное ``ID`` будет отрицательным (для                              |
|    :ref_prefix: ep_OnAfterCopyToLive_ | :doc:`подчинённых записей </components/working_with_sub_prefixes>`) |
|                                       | или нулём (для                                                      |
|                                       | :doc:`главных записей </components/working_with_sub_prefixes>`) в   |
|                                       | случае, когда запись была создана во временной таблице и ещё не     |
|                                       | была скопирована в оригинальную таблицу.                            |
+---------------------------------------+---------------------------------------------------------------------+

.. note::

   Объекты, которые будут получены из событий, вызываемых из класса ``kTempTablesHandler`` никогда
   не содержат достоверной информации.

Поэтому в случае, когда нужен объект, загруженный по ``ID`` скопированной записи, то его нужно
загружать самому. Это будет показано на ниже приведённом примере.

.. code:: php

   $object =& $this->Application->recallObject($event->Prefix . '.-item', null, Array ('skip_autoload' => true));
   /* @var $object kDBItem */

   $object->SwitchToLive(); // для того, чтобы объект был загружен из оригинальной таблицы, а не из временной
   $object->Load( $event->getEventParam('id') );

Потенциальное применение
------------------------

Данное событие можно использовать для автоматического обновления или добавления данных в другие таблицы
на основе только что сохранённых в оригинальную таблицу данных. Это примерно тоже самое, что и используя
параметр :ref:`ep_OnSave_ids` события :doc:`/events/temp_editing/on_save`, но только здесь можно работать
с ``ID`` также и :doc:`подчинённых записей </components/working_with_sub_prefixes>`. Ниже приведён пример
добавления записи в журнал изменений:

.. code:: php

   function OnAfterCopyToLive(&$event)
   {
       parent::OnAfterCopyToLive($event);

       $log_object =& $this->Application->recallObject('log');
       /* @var $log_object kDBItem */

       $log_object->addEntry($event->Prefix, $event->getEventParam('id'));
   }

Ограничения
-----------

Данное событие будет вызываться только при использовании события :doc:`/events/temp_editing/on_save`,
и следовательно будет работать только в случае, когда используются
:doc:`временные таблицы </database/using_temporary_tables>`.

.. versionchanged:: 4.2.1

Это событие вызывается и в случае, когда у префикса нету
:doc:`подчинённых префиксов </components/working_with_sub_prefixes>`.

.. seealso::

   - :doc:`/database/using_temporary_tables`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnAfterCopyToLive
