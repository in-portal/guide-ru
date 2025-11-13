OnEdit
======
`Data Source`_

Данное событие создаёт структуру пустых :doc:`временных таблиц </database/using_temporary_tables>` и заполняет
их данными, полученными по ``IDs`` выбранных в списке на редактирование записей.

Вызывается из шаблона
---------------------

Данное событие вызывается при нажатии на кнопку ``Edit`` (редактирование выбранных записей) на панели инструментов
в списке :doc:`главных записей </components/working_with_sub_prefixes>`. Это реализуется через вызов ``JavaScript``
функции ``std_edit_item``. В случае, когда кнопка редактирования выбранных записей расположена на списке
:doc:`подчинённых записей </components/working_with_sub_prefixes>`, то никакого события вызвано не будет и будет
использоваться ``JavaScript`` функция ``std_edit_temp_item``.

Вызывает события
----------------

Данное событие косвенно (через метод ``kTempTablesHandler::PrepareEdit``) вызывает событие
:doc:`/events/temp_editing/on_after_copy_to_temp`.

Ограничения
-----------

Данное событие будет работать только в случае, когда используются
:doc:`временные таблицы </database/using_temporary_tables>`.

.. seealso::

   - :doc:`/database/using_temporary_tables`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnEdit
