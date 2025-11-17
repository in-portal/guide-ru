OnBeforeDeleteFromLive
======================
`Data Source`_

Данное событие вызывается индивидуально для каждой записи перед её удалением из оригинальной таблицы
и до её замещения записью из :doc:`временной таблицы </database/using_temporary_tables>`.

Вызывается из событий
---------------------

Данное событие косвенно (через метод ``kTempTablesHandler::DoCopyTempToOriginal``) вызывается из
события :doc:`/events/temp_editing/on_save` в процессе копирования данных из
:doc:`временной таблицы </database/using_temporary_tables>` в оригинальную.

Входные параметры
-----------------

+--------------------------------------------+-----------------------------------------------------------------------+
| название                                   | описание                                                              |
+============================================+=======================================================================+
| .. config-property::                       | ``ID`` записи во                                                      |
|    :name: id                               | :doc:`временной таблице </database/using_temporary_tables>`. Данное   |
|    :type: int                              | ``ID`` будет отрицательным (для                                       |
|    :ref_prefix: ep_OnBeforeDeleteFromLive_ | :doc:`подчинённых записей </components/working_with_sub_prefixes>`)   |
|                                            | или нулём (для                                                        |
|                                            | :doc:`главных записей </components/working_with_sub_prefixes>`) в     |
|                                            | случае, когда запись была создана во временной таблице и ещё не       |
|                                            | была скопирована в оригинальную таблицу.                              |
+--------------------------------------------+-----------------------------------------------------------------------+
| .. config-property::                       | Данный необязательный для                                             |
|    :name: foreign_key                      | :doc:`главных записей </components/working_with_sub_prefixes>`        |
|    :type: int                              | параметр содержит значение поля, по которому удаляемый объект связан  |
|    :ref_prefix: ep_OnBeforeDeleteFromLive_ | его                                                                   |
|                                            | :doc:`родительской записью </components/working_with_sub_prefixes>`.  |
|                                            | Данное значение получается из метода                                  |
|                                            | ``kTempTablesHandler::GetForeignKeys``.                               |
+--------------------------------------------+-----------------------------------------------------------------------+

.. note::

   Объекты, которые будут получены из событий, вызываемых из класса ``kTempTablesHandler`` никогда не
   содержат достоверной информации.

Поэтому в случае, когда нужен объект, загруженный по ``ID`` скопированной записи, то его нужно загружать
самому. Это будет показано на ниже приведённом примере.

.. code:: php

   $object =& $this->Application->recallObject($event->Prefix . '.-item', null, Array ('skip_autoload' => true));
   /* @var $object kDBItem */

   $object->Load( $event->getEventParam('id') );

Потенциальное применение
------------------------

Данное событие можно использовать для сохранения данных, которые находятся в оригинальной таблице.
К примеру можно сохранить оригинальные данные и далее сравнить их с новыми и выслать оповещения о
каких либо критичных изменениях. Если :ref:`ep_OnBeforeDeleteFromLive_id` меньше или равно нулю, то
запись ещё не была скопирована в оригинальную таблицу и оповещать никого конечно не нужно. Это будет
показано на ниже приведённом примере.

.. code:: php

   function OnBeforeDeleteFromLive(&$event)
   {
       parent::OnBeforeDeleteFromLive($event);

       $object =& $this->Application->recallObject($event->Prefix . '.-item', null, Array ('skip_autoload' => true));
       /* @var $object kDBItem */

       $object->Load( $event->getEventParam('id') );

       if ($event->getEventParam('id') <= 0) {
           return ;
       }

       $prev_data = $this->Application->GetVar('prev_info');
       if (!$prev_data) {
           $prev_data = Array ();
       }

       $prev_data[ $object->GetID() ] = $object->GetFieldValues();
       $this->Application->SetVar('prev_info', $prev_data);
   }

Ограничения
-----------

Данное событие будет вызываться только при использовании события :doc:`/events/temp_editing/on_save`, и
следовательно будет работать только в случае, когда используются
:doc:`временные таблицы </database/using_temporary_tables>`.

.. seealso::

   - :doc:`/database/using_temporary_tables`

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnBeforeDeleteFromLive
