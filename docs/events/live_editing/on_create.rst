OnCreate
========
`Data Source`_

.. include:: /includes/not_finished.rst

Используется для создания новой записи.

Вызывается из шаблона
---------------------

Вызывается из шаблона редактирования записи.

Вызывает события
----------------

в процессе выполнения вызывает события

- :doc:`/events/modify_data/on_before_item_create`

косвенно вызывает события через метод ``kDBItem::Create``:

- :doc:`/events/modify_data/on_before_item_validate`
- ``kDBItem::Validate``
- :doc:`/events/modify_data/on_after_item_validate`

В методе ``kDBItem::Create`` происходит базовая проверка объекта с помощью настроенных для них валидаторов,
форматирование элементов с помощью настроенных форматтеров и создание записи. В случае успешного создания записи,
вызывается следующий метод:

- :doc:`/events/modify_data/on_after_item_create`

Потенциальное применение
------------------------

Переписав данное событие в своем EventHandler, возможно сделать:

- выполнения дополнительных проверок значений полей объекта;
- установки значений полей, которые не доступны на форме редактирования;
- запрета создания записи в базе данных.
- отсылку дополнительных E-mails привязанных к специфическим условиям создания записи.

но не стоит забывать про методы ``OnBeforeItemCreate`` и ``OnAfterItemCreate``. Пример использования можно просмотреть
в platform, файл ``core/units/users/users_event_handler.php``.

Ограничения
-----------

...

.. seealso::

   - :doc:`/application_structure/system_classes/working_with_kdbitem_class`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnCreate
