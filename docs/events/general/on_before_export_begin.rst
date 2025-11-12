OnBeforeExportBegin
===================
`Data Source`_

.. include:: /includes/not_finished.rst

Событие ``OnBeforeExportBegin`` применяется только в административной консоли. В базовом классе событие
представлено пустым методом, который можно переопределять с целью модификации и дополнительных проверок
параметров экспорта/импорта.

Вызывается из шаблона
---------------------

Не вызывается из шаблона.

Вызывается из событий
---------------------

- :doc:`/events/general/on_export_begin`

Входные параметры
-----------------

+----------------------+-----------------------------+
| название             | описание                    |
+======================+=============================+
| .. config-property:: | Параметры экспорта/импорта. |
|    :name: options    |                             |
|    :type: array      |                             |
+----------------------+-----------------------------+

Вызывает события
----------------

Не вызывает событий.

Потенциальное применение
------------------------

Модификации и дополнительные проверки параметров экспорта/импорта, требуемые в конкретной реализации
экспорта/импорта в отличие от стандартного экспорта/импорта. Например - добавление новых параметров.

.. code:: php

   $options = $event->getEventParam('options') ;

   $items_list =& $this->Application->recallObject($event->Prefix.'.'.$this->Application->RecallVar('export_oroginal_special'), $event->Prefix.'_List');
   $items_list->SetPerPage(-1);
   if ($options['export_ids'] != '') {
       $items_list->AddFilter('export_ids', $items_list->TableName.'.'.$items_list->IDField.' IN ('.implode(',',$options['export_ids']).')');
   }

   $options['ForceCountSQL'] = $items_list->getCountSQL( $items_list->GetSelectSQL(true,false) );
   $options['ForceSelectSQL'] = $items_list->GetSelectSQL();

   $event->setEventParam('options',$options);

Это пример для экспорта заказов (из класса ``OrdersEventHandler``). В нём формируются параметры, содержащие
SQL-запросы для извлечения и подсчёта экспортируемых записей, и сохраняются в передаваемом по ссылке объекте
``$event``.

Ограничения
-----------

Ограничений нет.

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnBeforeExportBegin
