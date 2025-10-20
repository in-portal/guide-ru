OnSelectUser
============
`Data Source`_

.. include:: /includes/not_finished.rst

Используется при выборки ID пользователя из списка.

Вызывается из шаблона
---------------------

Вызывается из формы редактирования, для использования этого метода существует блок :ref:`form_control_inp_edit_user`.

Вызывает события
----------------

- ``kDBEventHandler::RemoveRequiredFields`` отключает все required поля
- если форма открыта для создания записи то вызывает метод :doc:`kDBItem::Create </application_structure/system_classes/working_with_kdbitem_class>`
- если форма открыта для изменения записи то вызывает метод :doc:`kDBItem::Update </application_structure/system_classes/working_with_kdbitem_class>`

Потенциальное применение
------------------------

Можно использовать для изменения метода сохранения выбранного пользователя или для дополнительных
проверок при выборе пользователя.

Ограничения
-----------

Метод использует :doc:`временные таблицы </database/using_temporary_tables>`.

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnSelectUser
