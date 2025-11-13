OnAfterCopyToTemp
=================
`Data Source`_

Данное событие вызывается индивидуально для каждой записи после её копирования из оригинальной таблицы
во временную таблицу.

Вызывается из событий
---------------------

Данное событие косвенно (через метод ``kTempTablesHandler::DoCopyLiveToTemp``) вызывается из события
:doc:`/events/temp_editing/on_edit` в процессе копирования данных из оригинальной таблицы во
:doc:`временную </database/using_temporary_tables>`.

Входные параметры
-----------------

+----------------------+---------------------------------------+
| название             | описание                              |
+======================+=======================================+
| .. config-property:: | ``ID`` записи в оригинальной таблице. |
|    :name: id         |                                       |
|    :type: int        |                                       |
+----------------------+---------------------------------------+

.. note::

   Объекты, которые будут получены из событий, вызываемых из класса ``kTempTablesHandler`` никогда
   не содержат достоверной информации.

Поэтому в случае, когда нужен объект, загруженный по ``ID`` скопированной записи, то его нужно
загружать самому. Это будет показано на ниже приведённом примере.

.. code:: php

   $object =& $this->Application->recallObject($event->Prefix . '.-item', null, Array ('skip_autoload' => true));
   /* @var $object kDBItem */

   $object->Load( $event->getEventParam('id') );

Потенциальное применение
------------------------

Данное событие может применяться при необходимости сделать какие-либо действия с данными во
:doc:`временной таблице </database/using_temporary_tables>`. К примеру для выставления флага,
что данная запись редактируется, таким образом можно запретить одновременное редактирование
одной записи двумя :doc:`пользователями </database/table_structure/portal_user>`.

.. code:: php

   function OnAfterCopyToTemp(&$event)
   {
       parent::OnAfterCopyToTemp($event);

       $id_field = $this->Application->getUnitOption($event->Prefix, 'IDField');
       $table_name = $this->Application->getUnitOption($event->Prefix, 'TableName');

       $sql = 'UPDATE ' . $table_name . '
               SET InEdit = 1
               WHERE ' . $id_field . ' = ' . $event->getEventParam('id');
       $this->Conn->Query($sql);
   }

Ограничения
-----------

Данное событие будет вызываться только при использовании события :doc:`/events/temp_editing/on_edit`,
и следовательно будет работать только в случае, когда используются
:doc:`временные таблицы </database/using_temporary_tables>`.

.. seealso::

   - :doc:`/database/using_temporary_tables`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnAfterCopyToTemp
