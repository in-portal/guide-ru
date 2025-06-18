Работа классом MInputHelper
===========================
`Data Source`_

.. versionadded:: 4.2.2

.. figure:: /images/Minput_control.jpg
   :figwidth: 180px
   :width: 180px
   :align: left
   :alt: Визуальный пример вывода блока "inp_edit_minput"

   Визуальный пример вывода блока "inp_edit_minput"

Данный класс предназначен для ввода списка дополнительных данных в схожем формате, характеризующих основной предмет.
Например, человек (``people``) - это пример основной сущности, а список его детей (``children``) - это пример
дополнительной сущности. Т.е. ребенок (``children``) это подчинённый префикс для главного префикса ``people``.
Процесс ввода данных происходит по средствам использования блока ``inp_edit_minput``, который показан на изображении
слева.

.. clear-float::

Базовая настройка
-----------------

Редактирование файла people_config.php
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Определить поле ``Children``, используемое для хранения данных в ``XML`` формате. Поле в
:doc:`базе данных </database/using_database>` нужно сделать с типом ``TEXT``.

.. code:: php

   'Fields' => Array (
       'Children' => Array ('type' => 'string', 'default' => NULL),
   )

XML документ находящийся в данном поле будет выглядеть следующим образом:

.. code:: xml

   <records>
       <record>
           <field name="ChildFullName">name1</field>
           <field name="ChildBirthDate_date">15/12/2008</field>
       </record>
       <record>
           <field name="ChildFullName">name2</field>
           <field name="ChildBirthDate_date">19/04/2005</field>
       </record>
   </records>

На самом деле такого оформления, как в примере не будет, а все данные будут находиться в одной строке.

Определить виртуальные поля ``ChildFullName`` и ``ChildBirthDate``, которые нужны только для редактирования
элементов, показываемых в списке из блока ``inp_edit_minput``.

.. code:: php

   'VirtualFields' => Array (
       'ChildFullName' => Array ('type' => 'string', 'max_len' => 255, 'default' => ''),
       'ChildBirthDate' => Array ('type' => 'int', 'formatter' => 'kDateFormatter', 'default' => ''),
   )

Редактирование файла people_edit.tpl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

В данном файле нужно добавить блоки, которые будут использоваться для ввода данных в блок ``inp_edit_minput``:

.. code:: html

   <inp2:m_RenderElement name="inp_edit_box" prefix="people" field="ChildFullName" title="la_fld_ChildFullName" style="width: 200px;" />
   <inp2:m_RenderElement name="inp_edit_date" prefix="people" field="ChildBirthDate" title="la_fld_ChildBirthDate" style="width: 100px"/>
   <inp2:m_RenderElement name="inp_edit_minput" prefix="people" field="Children" title="la_fld_Children" format="#ChildFullName# #ChildBirthDate_date#" />

Блок ``inp_edit_minput`` нужен для того, чтобы в поле ``Children`` (у главного префикса) формировался ``XML``,
который в последствии может быть обработан (через :doc:`hook </components/unit_configs/hooks>`) и записан в
подчинённую таблицу.

После определения всех блоков формы, нужно поместить следующий ``JavaScript`` код, использующийся для связи
остальных элементов формы (в данном случае это элементы полей ``ChildFullName`` и ``ChildBirthDate``) с полем
``Children`` главного префикса:

.. code:: html

   <script type="text/javascript">
       Children.registerControl('ChildFullName', 'textbox', true);
       Children.registerControl('ChildBirthDate_date', 'textbox', true);
       Children.LoadValues();
   </script>

Метод ``registerControl`` используется для связи **одного поля** с блоком ``inp_edit_minput``. Если нужно связать
сразу несколько полей, то нужно вызвать данный метод несколько раз с разными параметрами. В метод ``registerControl``
передаются следующие далее параметры.

+-----------------------+-------------------------------------------------------------------------------------+
| название              | описание                                                                            |
+=======================+=====================================================================================+
| .. config-property::  | Название поля. Для поля, содержащего дату нужно к нему ещё приписать ``_date``.     |
|    :name: $field_name |                                                                                     |
|    :type: string      |                                                                                     |
+-----------------------+-------------------------------------------------------------------------------------+
| .. config-property::  | Тип HTML-элемента, используемого для ввода значений в поле:                         |
|    :name: $type       |                                                                                     |
|    :type: string      | - ``select`` - элемент ограниченного выбора (``dropdown``);                         |
|                       | - ``textbox`` - текстовое поле (``text``, ``texarea``).                             |
|                       |                                                                                     |
|                       | .. versionadded:: 5.0.0                                                             |
|                       |                                                                                     |
|                       | - ``checkbox``.                                                                     |
+-----------------------+-------------------------------------------------------------------------------------+
| .. config-property::  | Пометка об обязательности ввода значения в поле перед добавлением записи или при    |
|    :name: $required   | её редактировании.                                                                  |
|    :type: bool        |                                                                                     |
+-----------------------+-------------------------------------------------------------------------------------+
| .. config-property::  | .. versionadded:: 5.0.0                                                             |
|    :name: $options    |                                                                                     |
|    :type: array       | Массив опций поля. Для элемента типа ``checkbox`` это                               |
|                       | :ref:`массив опций форматера <fmt_options>`. Для текстовых полей там можно          |
|                       | указать ``{first_chars: 100}`` и тогда показываемое значение из данного поля        |
|                       | будет визуально ограничено 100 символами. Данный параметр является необязательным.  |
+-----------------------+-------------------------------------------------------------------------------------+

После всех выше описанных операций нужно вызвать метод ``LoadValues``, используемый для преобразования XML данных,
находящихся в поле и показывания их в блоке ``inp_edit_minput``.

Параметры блока "inp_edit_minput"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ниже приведено описание параметров блока ``inp_edit_minput``. Параметры ``name``, ``prefix``, ``field``, ``title``
и ``style`` являются стандартными для всех блоков, используемых на формах редактирования, поэтому в данной статье
они описаны не будут.

+------------------------+--------------------------------------------------------------------------------------+
| параметр               | описание                                                                             |
+========================+======================================================================================+
| .. config-property::   | Значением данного параметра является строка, которая может состоять из названий      |
|    :name: format       | полей (зарегистрированных в шаблоне при помощи метода ``registerControl``) и         |
|    :type: string       | любого текста. Название каждого поля должно быть заключено в символы ``#``.          |
|    :required: true     | Например ``"#ChildFullName# #ChildBirthDate_date#"``. Фразы использовать нельзя,     |
|                        | т.к. они не обрабатываются.                                                          |
+------------------------+--------------------------------------------------------------------------------------+
| .. config-property::   | Можно указать стиль для блока, обычно в данном случае ставиться стиль размера блока, |
|    :name: style        | например ``style="width: 400px; height: 100px;"``.                                   |
|    :type: string       |                                                                                      |
+------------------------+--------------------------------------------------------------------------------------+
| .. config-property::   | Можно разрешить/запретить добавление элементов списка, по умолчанию разрешено.       |
|    :name: allow_add    |                                                                                      |
|    :type: int          |                                                                                      |
+------------------------+--------------------------------------------------------------------------------------+
| .. config-property::   | Можно разрешить/запретить редактирование элементов списка, по умолчанию разрешено.   |
|    :name: allow_edit   |                                                                                      |
|    :type: int          |                                                                                      |
+------------------------+--------------------------------------------------------------------------------------+
| .. config-property::   | Можно разрешить/запретить удаление элементов списка, по умолчанию разрешено.         |
|    :name: allow_delete |                                                                                      |
|    :type: int          |                                                                                      |
+------------------------+--------------------------------------------------------------------------------------+
| .. config-property::   | .. versionadded:: 4.3.1                                                              |
|    :name: allow_move   |                                                                                      |
|    :type: int          | Можно разрешить/запретить перемещение элементов вверх и вниз в списке, по умолчанию  |
|                        | разрешено.                                                                           |
|                        |                                                                                      |
|                        | .. caution::                                                                         |
|                        |                                                                                      |
|                        |    В зависимости от того, как будет обрабатываться полученный                        |
|                        |    :doc:`XML </application_structure/helper_classes/xml_document_handling>`          |
|                        |    может получиться, что в базе данных ничего перемещаться не будет.                 |
+------------------------+--------------------------------------------------------------------------------------+

.. note::

   ``*`` - Параметр обязателен

Хранение данных в связанной таблице
-----------------------------------

Возможна ситуация, когда нужно хранить данные в отдельной, связанной таблице, при помощи которой можно будет,
например делаться поиск по данным. В таком случае требуется дополнительно выполнить все ниже указанные действия.

Редактирование конфигурационных файлов
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Нужно отредактировать конфигурационные файлы для главного префикса ``people`` и подчинённого префикса ``children``.

а) файл ``people_config.php``:

.. code:: php

   'IDField' => 'PeopleId',
   'SubItems' => Array ('children'),

   'VirtualFields' => Array (
       'PeopleId' => Array ('type' => 'int', 'not_null' => 1, 'default' => 0),
       'ChildFullName' => Array ('type' => 'string', 'max_len' => 255, 'default' => NULL),
       'ChildBirthDate' => Array ('type' => 'int', 'formatter' => 'kDateFormatter', 'default' => NULL),
       'Children' => Array ('type' => 'string', 'default' => NULL),
   ),

В выше приведённом примере устанавливается значение ``IDField``, подчиненный префикс ``children``, а также
описываются виртуальные поля ``ChildFullName`` и ``ChildBirthDate`` для главного префикса ``people``. Эти поля
аналогичны полям из префикса ``children``, только в данном случае они виртуальные. Поле ``Children`` нужно для
загрузки ``XML`` структуры списка детей.

б) файл ``children_config.php``:

Нужно установить связь с главным префиксом ``people``, в параметре :ref:`uc_Fields` описать поля для подчинённого
префикса ``children``. И установить :doc:`hook </components/unit_configs/hooks>`, который нужен для сохранения
данных в подчинённую таблицу при сохранении главной записи.

.. code:: php

   'Hooks' => Array (
       Array (
           'Mode' => hAFTER,
           'Conditional' => false,
           'HookToPrefix' => '#PARENT#',
           'HookToSpecial' => '*',
           'HookToEvent' => Array ('OnAfterItemCreate', 'OnAfterItemUpdate'),
           'DoPrefix' => '',
           'DoSpecial' => '*',
           'DoEvent' => 'OnSaveChildren',
       ),
   ),

   'ForeignKey' => 'PeopleId',
   'ParentTableKey' => 'PeopleId',
   'ParentPrefix' => 'people',
   'AutoDelete' => true,
   'AutoClone' => true,

   'Fields' => Array(
       'ChildId' => Array ('type' => 'int', 'not_null' => 1, 'default' => 0),
       'PeopleId' => Array ('type' => 'int', 'not_null' => 1, 'default' => 0),
       'ChildFullName' => Array ('type' => 'string', 'max_len' => 255, 'default' => ''),
       'ChildBirthDate' => Array ('type' => 'int', 'formatter' => 'kDateFormatter', 'default' => NULL)
   ),

Редактирование обработчиков событий
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

а) Добавить метод :doc:`/events/modify_data/on_after_item_load` в файле ``people_eh.php``.

.. code:: php

   function OnAfterItemLoad(&$event)
   {
       parent::OnAfterItemLoad($event);

       $minput_helper =& $this->Application->recallObject('MInputHelper');
       /* @var $minput_helper MInputHelper */

       $use_fields = Array ('ChildFullName', 'ChildBirthDate_date');
       $minput_helper->LoadValues($event, 'Children', 'children', $use_fields);
   }

Используемый метод ``LoadValues`` класса ``MInputHelper`` нужен для формирования XML строки из подчинённой
таблицы и помещения его в поле ``Children`` главного префикса.

б) Добавить метод ``OnSaveChildren`` в файле ``children_eh.php``.

.. code:: php

   function OnSaveChildren(&$event)
   {
       if ($event->MasterEvent->status != erSUCCESS) {
           return ;
       }

       $minput_helper =& $this->Application->recallObject('MInputHelper');
       /* @var $minput_helper MInputHelper */

       $minput_helper->SaveValues($event, 'Children');
   }

Данный :doc:`hook </components/unit_configs/hooks>` к главному префиксу (см. выше) нужен для сохранения в базу
данных сведений о детях. Для этих целей используется метод ``SaveValues`` класса ``MInputHelper``.

.. seealso::

   - :doc:`/admin_console_ui/forms/editpickerhelper_class`

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0_%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%BE%D0%BC_MInputHelper
