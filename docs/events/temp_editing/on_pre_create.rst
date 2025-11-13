OnPreCreate
===========
`Data Source`_

Данное событие создаёт структуру пустых :doc:`временных таблиц </database/using_temporary_tables>` а
также инициализирует поля объекта :doc:`главной записи </components/working_with_sub_prefixes>` значениями
по умолчанию (не создаёт его в базе данных). Также данное событие переключает редактирование в режим работы
с созданными ранее временными таблицами.

Вызывается из шаблона
---------------------

Данное событие вызывается при нажатии на кнопку ``Add`` (добавление новой записи) на панели инструментов в
списке :doc:`главных записей </components/working_with_sub_prefixes>`. Это реализуется через вызов
``JavaScript`` функции ``std_precreate_item``. В случае, когда кнопка добавления новой записи расположена на
списке :doc:`подчинённых записей </components/working_with_sub_prefixes>`, то будет вызвано событие
:doc:`/events/live_editing/on_new` и будет использоваться ``JavaScript`` функция ``std_new_item``.

Потенциальное применение
------------------------

Данное событие можно использовать для динамической установки значений по умолчанию для полей объекта. Также
динамическую установку значений по умолчанию можно делать из события :doc:`/events/general/on_after_config_read`.
Это нагляднее будет продемонстрировано на ниже приведённом примере.

.. code:: php

   function OnPreCreate(&$event)
   {
       parent::OnPreCreate($event);

       $object =& $event->getObject();
       /* @var $object kDBItem */

       $object->SetDBField('SampleField_date', strtotime('-1 day'));
       $object->SetDBField('SampleField_time', strtotime('-1 day'));
   }

Ограничения
-----------

Данное событие будет работать только в случае, когда используются
:doc:`временные таблицы </database/using_temporary_tables>`.

.. seealso::

   - :doc:`/database/using_temporary_tables`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnPreCreate
