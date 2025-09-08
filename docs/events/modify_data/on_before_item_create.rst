OnBeforeItemCreate
==================
`Data Source`_

Данное событие позволяет выполнить дополнительные действия перед созданием новой записи в базе данных.
Это событие вызывается до того, как выполняется проверка (``validation``) значений в полях объекта.

Вызывается из событий
---------------------

Данное событие косвенно вызывается из событий, создающих новые записи: :doc:`/events/live_editing/on_create`,
:doc:`/events/onpresave/on_pre_save_created`, :doc:`/events/onpresave/on_pre_save_and_open_translator`,
:doc:`/events/onpresave/on_pre_save_sub_item`. Все ранее упомянутые события в свою очередь вызывают метод
``kDBItem::Create``, который при помощи метода ``kDBItem::raiseEvent`` вызывает данное событие. Более детально
это продемонстрировано ниже:

.. code::

   OnCreate -> kDBItem::Create -> kDBItem::raiseEvent

Потенциальное применение
------------------------

Данное событие можно использовать для

- выполнения дополнительных проверок значений полей объекта;
- установки значений полей, которые не доступны на форме редактирования;
- запрета создания записи в базе данных.

Ниже будет приведён пример, в котором показано как можно использовать все описанные приёмы.

.. code:: php

   function OnBeforeItemCreate(&$event)
   {
       parent::OnBeforeItemCreate($event);

       $object =& $event->getObject();
       /* @var $object kDBItem */

       if ($object->GetDBField('Name') != 'John') {
           // если значение поля Name не равно John, то показывать специфическую (не стандартную) ошибку
           $object->SetError('Name', 'invalid_name', 'la_error_OnlyJohnsAllowed');
       }

       // запоминание времени создания записи
       $now = adodb_mktime();
       $object->SetDBField('CreatedOn_date', $now);
       $object->SetDBField('CreatedOn_time', $now);

       if ($object->GetDBField('Status') != STATUS_ACTIVE) {
           // можно создавать записи только с активным статусом
           $event->status = erFAIL;
       }
   }

Ограничения
-----------

Если статус события (``$event->status``), по его завершении, не будет равен :ref:`const_erSUCCESS`, то событие
:doc:`/events/modify_data/on_after_item_create` вызвано не будет и запись не будет создана в базе данных.

.. seealso::

   - :doc:`/application_structure/system_classes/working_with_kdbitem_class`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnBeforeItemCreate
