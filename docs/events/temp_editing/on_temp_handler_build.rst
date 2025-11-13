OnTempHandlerBuild
==================
`Data Source`_

Данное событие используется для инициализации объектов, созданных из класса ``kTempTablesHandler``.
В последствии настроенный при помощи этого события объект можно будет использовать для работы с
:doc:`временными таблицами </database/using_temporary_tables>`. По окончании своей работы в созданном
объекте будет доступна иерархическая структура главного и подчинённых :ref:`префиксов <uc_Prefix>`.

Вызывается из событий
---------------------

Данное событие вызывается из всех событий, которые используют услуги класса ``kTempTablesHandler``, а именно:

- :doc:`/events/live_editing/on_delete` - удаление одной записи;
- :doc:`/events/lists/on_delete_all` - удаление всех записей;
- :doc:`/events/live_editing/on_cancel`;
- :doc:`/events/lists/on_mass_delete` - удаление выбранных записей;
- :doc:`/events/temp_editing/on_edit`;
- :doc:`/events/temp_editing/on_save`;
- :doc:`/events/temp_editing/on_cancel_edit`;
- :doc:`/events/temp_editing/on_pre_create`;
- :doc:`/events/lists/on_mass_clone` - клонирование выбранных записей.

Потенциальное применение
------------------------

Данное событие будет автоматически вызвано при выполнении из любого :doc:`события </events>` ниже
приведённого кода. В следствие чего вызывать его в ручную не требуется.

.. code:: php

   $temp_handler =& $this->Application->recallObject(
       $event->getPrefixSpecial() . '_TempHandler',
       'kTempTablesHandler'
   );
   /* @var $temp_handler kTempTablesHandler */

.. seealso::

   - :doc:`/database/using_temporary_tables`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnTempHandlerBuild
