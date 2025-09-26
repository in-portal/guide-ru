OnBeforeItemDelete
==================
`Data Source`_

Данное событие позволяет выполнить дополнительные действия перед удалением записи из базы данных.

Вызывается из событий
---------------------

Данное событие косвенно вызывается из событий, удаляющих записи: :doc:`/events/live_editing/on_delete`,
:doc:`/events/lists/on_delete_all`, :doc:`/events/lists/on_mass_delete`. Все ранее упомянутые события в
свою очередь вызывают метод ``kTempTablesHandler::DeleteItems``, который при помощи метода ``kDBItem::raiseEvent``
вызывает данное событие. Более детально это продемонстрировано ниже:

.. code::

   OnDelete -> kTempTablesHandler::DeleteItems -> kDBItem::Delete -> kDBItem::raiseEvent

Входные параметры
-----------------

+----------------------+-------------------------------------------------------------+
| название             | описание                                                    |
+======================+=============================================================+
| .. config-property:: | ``ID`` той записи, для которой поступил запрос на удаление. |
|    :name: id         |                                                             |
|    :type: int        |                                                             |
+----------------------+-------------------------------------------------------------+

Потенциальное применение
------------------------

Данное событие в основном применяется для проверки того, что пользователю разрешено удалять конкретную запись.
Как это сделать продемонстрировано на ниже приведённом примере.

.. code:: php

   function OnBeforeItemDelete(&$event)
   {
       parent::OnBeforeItemDelete($event);

       $object =& $event->getObject();
       /* @var $object kDBItem */

       if ($object->GetDBField('Status') != STATUS_ACTIVE) {
           // можно удалять только активные записи
           $event->status = erFAIL;
       }
   }

В случае, когда запись, из выше приведённого примера, будет не активной, то она не будет удалена и событие
:doc:`/events/modify_data/on_after_item_delete` также не будет вызвано.

.. seealso::

   - :doc:`/application_structure/system_classes/working_with_kdbitem_class`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnBeforeItemDelete
