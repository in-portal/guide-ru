OnBeforeItemUpdate
==================
`Data Source`_

Данное событие позволяет выполнить дополнительные действия до сохранения изменённой записи в базу данных.
Это событие вызывается до того, как выполняется проверка (``validation``) значений в полях объекта.

Вызывается из событий
---------------------

Данное событие косвенно вызывается из событий, изменяющих (созданные ранее) записи:
:doc:`/events/live_editing/on_update`, :doc:`/events/onpresave/on_pre_save`. Все ранее упомянутые события в
свою очередь вызывают метод ``kDBItem::Update``, который при помощи метода ``kDBItem::raiseEvent`` вызывает
данное событие. Более детально это продемонстрировано ниже:

.. code::

   OnUpdate -> kDBItem::Update -> kDBItem::raiseEvent

Входные параметры
-----------------

+----------------------+-------------------------------------------------------------------------+
| название             | описание                                                                |
+======================+=========================================================================+
| .. config-property:: | ``ID`` той записи, которая будет в последствии сохранена в базу данных. |
|    :name: id         |                                                                         |
|    :type: int        |                                                                         |
+----------------------+-------------------------------------------------------------------------+

Потенциальное применение
------------------------

Данное событие можно использовать для

- выполнения дополнительных проверок значений полей объекта;
- установки значений полей, которые не доступны на форме редактирования;
- запрета изменения записи в базе данных.

Ниже будет приведён пример, в котором показано как можно использовать все описанные приёмы.

.. code:: php

   function OnBeforeItemUpdate(&$event)
   {
       parent::OnBeforeItemUpdate($event);

       $object =& $event->getObject();
       /* @var $object kDBItem */

       if ($object->GetDBField('Name') != 'John') {
           // если значение поля Name не равно John, то показывать специфическую (не стандартную) ошибку
           $object->SetError('Name', 'invalid_name', 'la_error_OnlyJohnsAllowed');
       }

       // запоминание времени изменения записи
       $now = adodb_mktime();
       $object->SetDBField('ModifiedOn_date', $now);
       $object->SetDBField('ModifiedOn_time', $now);

       if ($object->GetDBField('Status') != STATUS_ACTIVE) {
           // можно изменять только активные записи
           $event->status = erFAIL;
       }
   }

Ограничения
-----------

Если статус события (``$event->status``), по его завершении, не будет равен :ref:`const_erSUCCESS`, то событие
:doc:`/events/modify_data/on_after_item_update` вызвано не будет и запись не будет изменена в базе данных.

.. seealso::

   - :doc:`/application_structure/system_classes/working_with_kdbitem_class`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnBeforeItemUpdate
