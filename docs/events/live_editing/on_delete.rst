OnDelete
========
`Data Source`_

.. include:: /includes/not_finished.rst

Используется для удаления одиночной записи.

Вызывается из шаблона
---------------------

Вызывается из шаблонов FrontEnd, например из списка Items в котором имеется кнопка или ссылка с параметром
event=OnDelete и ID удаляемой записи.

Потенциальное применение
------------------------

Переписав данный метод в своем EventHandler, возможно поменять условия удаления необходимой записи или сделать
дополнительные проверки при удалении записи. Пример: По условиям задачи необходимо проверить, что удаляемая
запись была создана тем пользователем, который ее удаляет. Для этого каждой записи существует поле CreatorID
в котором хранится ID хозяина этой записи.

.. code:: php

   /**
    * Delete's kDBItem object
    *
    * @param kEvent $event
    * @access protected
    */
   function OnDelete(&$event)
   {
       // проверка на то, что текущий пользователь не имеет прав READONLY
       if ($this->Application->CheckPermission('SYSTEM_ACCESS.READONLY', 1)) {
           return;
       }
       // создание экземпляра объекта
       $temp =& $this->Application->recallObject($event->getPrefixSpecial().'_TempHandler', 'kTempTablesHandler');
       /* @var $temp kTempTablesHandler */

       //Получаем ID текущего пользователя
       $current_user_id = $this->Application->RecallVar('user_id');
       //Получаем ID хозяина записи
       $CreatorID = $temp->GetDbField('CreatorID');
       //сравниваем полученный ID с ID хозяина записи
       if ($current_user_id != $CreatorID) {
           return;
       }

       // удаление записи
       $temp->DeleteItems($event->Prefix, $event->Special, Array($this->getPassedID($event)));
   }


.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnDelete
