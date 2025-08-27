OnAfterItemValidate
===================
`Data Source`_

Данное событие вызывается после успешной проверки (``validation``) значений полей объекта.

Вызывается из событий
---------------------

Данное событие косвенно вызывается из всех событий изменяющих данные, а конкретнее из:

- :doc:`/events/live_editing/on_create`;
- :doc:`/events/live_editing/on_update`;
- :doc:`/events/onpresave/on_pre_save`;
- :doc:`/events/onpresave/on_pre_save_created`;
- :doc:`/events/onpresave/on_pre_save_sub_item`.

Более детально это продемонстрировано ниже:

.. code::

   OnCreate -> kDBItem::Create -> kDBItem::raiseEvent
   OnUpdate -> kDBItem::Update -> kDBItem::raiseEvent

Входные параметры
-----------------

+----------------------+---------------------------------------------------------------+
| название             | описание                                                      |
+======================+===============================================================+
| .. config-property:: | ``ID`` той записи, для которой выполнялась проверка её полей. |
|    :name: id         |                                                               |
|    :type: int        |                                                               |
+----------------------+---------------------------------------------------------------+

Потенциальное применение
------------------------

Данное событие можно использовать для изменений свойств объекта, будучи уверенным, что объект прошёл проверку
на ошибки с помощью метода |kdbitem_validate_link|.

Ограничения
-----------

Вызывается только в случае, когда метод |kdbitem_validate_link| завершился успешно успешно. Если статус
события (``$event->status``), по его завершении, не будет равен :ref:`const_erSUCCESS`, то запись в базе
данных не будет создана или изменена. Данное событие вызывается до того, как произойдёт обращение к базе
данных.

.. seealso::

   - :doc:`/application_structure/system_classes/working_with_kdbitem_class`

.. |kdbitem_validate_link| replace:: :doc:`kDBItem::Validate </application_structure/system_classes/working_with_kdbitem_class>`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnAfterItemValidate
