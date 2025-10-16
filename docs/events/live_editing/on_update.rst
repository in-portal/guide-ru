OnUpdate
========
`Data Source`_

.. include:: /includes/not_finished.rst

Событие применяется для сохранения изменённых данных, в основно используется в формах, но при необходимости может
вызываться и из кода при автоматическом изменении каких либо элементов объекта.

Вызывается из шаблона
---------------------

На административной части сайта вызывается при нажатии кнопки Save, если окно было открыто для редактирования.

Вызывает события
----------------

в процессе выполнения вызывает события

- :doc:`/events/modify_data/on_before_item_update`

Косвенно вызывает события через метод
:doc:`kDBItem::Update </application_structure/system_classes/working_with_kdbitem_class>`:

- :doc:`/events/modify_data/on_before_item_validate`
- :doc:`kDBItem::Validate </application_structure/system_classes/working_with_kdbitem_class>`
- :doc:`/events/modify_data/on_after_item_validate`

В методе :doc:`kDBItem::Validate </application_structure/system_classes/working_with_kdbitem_class>` происходит базовая
проверка объекта с помощью настроенных для них валидаторов, форматирование элементов с помощью настроенных форматтеров
и создание записи.

В случае успешного создания записи, вызывается следующий метод:

- :doc:`/events/modify_data/on_after_item_update`

Потенциальное применение
------------------------

Применяется для изменения записи данных в DB.

Не рекомендуется изменять этот метод, лучше воспользоваться возможностями
:doc:`/events/modify_data/on_before_item_update` и :doc:`/events/modify_data/on_after_item_update`.

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnUpdate
