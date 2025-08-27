OnAfterItemLoad
===============
`Data Source`_

Данное событие позволяет выполнить дополнительные действия после успешной загрузки объекта из базы данных.

Вызывается из событий
---------------------

Данное событие косвенно вызывается из события :doc:`/events/general/on_item_build` в тот момент, когда объект
автоматически загружается по ``ID``, переданному в запросе от пользователя. Также оно вызывается из метода
:doc:`kDBItem::Load </application_structure/system_classes/working_with_kdbitem_class>`. Более детально это
продемонстрировано ниже:

.. code::

   OnItemBuild -> kDBEventHandler::LoadItem -> kDBItem::Load -> kDBItem::raiseEvent

Входные параметры
-----------------

+----------------------+----------------------------------------------------------------------------------+
| название             | описание                                                                         |
+======================+==================================================================================+
| .. config-property:: | ``ID`` той записи, которая была успешно загружена из базы данных. Если в методе  |
|    :name: id         | уже используется загруженный объект, то лучше получить ``ID`` прямо у него:      |
|    :type: int        |                                                                                  |
|                      | .. code:: php                                                                    |
|                      |                                                                                  |
|                      |    $object =& $event->getObject();                                               |
|                      |    /* @var $object kDBItem */                                                    |
|                      |                                                                                  |
|                      |    $id = $object->GetID();                                                       |
+----------------------+----------------------------------------------------------------------------------+

Потенциальное применение
------------------------

Данное событие можно использовать для установки значений виртуальных полей объекта на основании его
реальных полей. Это будет показано на ниже приведённом примере.

.. code:: php

   function OnAfterItemLoad(&$event)
   {
       parent::OnAfterItemLoad($event);

       $object =& $event->getObject();
       /* @var $object kDBItem */

       $area = $object->GetDBField('Width') * $object->GetDBField('Height');
       $object->SetDBField('Area', $area);
   }

Ограничения
-----------

Данное событие вызывается только после успешной загрузки объекта из базы данных.

.. seealso::

   - :doc:`/application_structure/system_classes/working_with_kdbitem_class`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnAfterItemLoad
