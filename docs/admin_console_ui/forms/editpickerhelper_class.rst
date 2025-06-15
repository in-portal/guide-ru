Работа классом EditPickerHelper
===============================
`Data Source`_

.. versionadded:: 4.2.2

.. figure:: /images/Editpickerhelper.png
   :figwidth: 180px
   :width: 180px
   :align: left
   :alt: Изображение блока "inp_edit_picker" на форме редактирования.

   Изображение блока "inp_edit_picker" на форме редактирования.

Блок ``inp_edit_picker`` представляет из себя два поля в одном из которых находятся выбранные элементы, а во
втором все доступные элементы за исключением уже выбранных. Данный блок позволяет выбрать несколько элементов
одновременно и перенести их во второй список.

Класс *EditPickerHelper* автоматизирует обработку данных, полученных из блока ``inp_edit_picker``.

.. clear-float::

.. _using_editpickerhelper_on_template:

Использование на шаблоне
------------------------

Использовать блок ``inp_edit_picker`` в шаблоне можно следующим образом:

.. code:: html

   <inp2:m_RenderElement
       name="inp_edit_picker" prefix="sample-prefix" field="OptionField" title="la_fld_OptionField"
       optprefix="option-prefix" option_key_field="OptionId" option_value_field="OptionTitle"
       size="10" style="CSS definitions"
   />

Ниже приведено описание параметров блока ``inp_edit_picker``. Параметры ``name``, ``prefix``, ``field``, ``title``
и ``style`` являются стандартными для всех блоков, используемых на формах редактирования, поэтому в данной статье
они описаны не будут.

+------------------------------+-------------------------------------------------------------------------------------------+
| параметр                     | описание параметра                                                                        |
+==============================+===========================================================================================+
| .. config-property::         | :ref:`Префикс <uc_Prefix>`, данные которого будут использованы для заполнения списка      |
|    :name: optprefix          | доступных и выбранных опций.                                                              |
|    :type: string             |                                                                                           |
+------------------------------+-------------------------------------------------------------------------------------------+
| .. config-property::         | Поле, объявленное в :doc:`unit config </components/unit_configs/config_files>` префикса   |
|    :name: option_key_field   | опций (указанного в ``optprefix``), которое содержит идентификатор (``ID``) опции.        |
|    :type: string             |                                                                                           |
+------------------------------+-------------------------------------------------------------------------------------------+
| .. config-property::         | Поле, объявленное в :doc:`unit config </components/unit_configs/config_files>` префикса   |
|    :name: option_value_field | опций (указанного в ``optprefix``), которое содержит название опции.                      |
|    :type: string             |                                                                                           |
+------------------------------+-------------------------------------------------------------------------------------------+
| .. config-property::         | Количество показываемых опций без боковой полосы прокрутки. По умолчанию данный параметр  |
|    :name: size               | равен 15.                                                                                 |
|    :type: int                |                                                                                           |
+------------------------------+-------------------------------------------------------------------------------------------+

Базовая настройка
-----------------

Независимо от используемого типа хранения данных, полученных из блока ``inp_edit_picker`` необходимо выполнить
следующие **два** действия.

Прописать в :doc:`конфигурационном файле </components/unit_configs/config_files>` префикса описание поля, которое
будет использоваться для хранения данных, полученных из блока ``inp_edit_picker``:

.. code:: php

   $config = Array(
       'Prefix' => 'sample-prefix',

       'Fields' => Array (
           'OptionField' => Array (
               'type' => 'string',
               'formatter' => 'kOptionsFormatter', 'options_sql' => 'SELECT %1$s FROM ' . TABLE_PREFIX . 'OptionTable',
               'option_key_field' => 'OptionId', 'option_title_field' => 'OptionTitle',
               'required' => 1, 'not_null' => 1, 'default' => 0
           ),
       ),

       'Grids' => Array (
           'Default' => Array (
               'Icons' => Array ('default' => 'icon16_custom.gif'),
               'Fields' => Array(
                   'OptionField' => Array (
                       'title' => 'la_col_OptionField', 'data_block' => 'grid_picker_td',
                       'filter_block' => 'grid_picker_filter', 'header_block' => 'grid_column_title_no_sorting'
                   ),
               ),
           ),
       ),
   );

Учитывая форму хранения значений в поле ``OptionField`` ему не представляется возможным сделать осмысленную
сортировку. В следствие чего используется блок ``grid_column_title_no_sorting``, который убирает возможность
сортировки по полю.

.. note::

   В случае, когда данные будут храниться в отдельной таблице поле должно быть :ref:`виртуальным <uc_VirtualFields>`.

Прописать в шаблоне редактирования :ref:`тег <using_editpickerhelper_on_template>`, использующий данное поле.
К данному моменту результатом использования блока ``inp_edit_picker`` будут заполненные списки доступных и
выбранных опций, правда в обоих из них будет полных список опций. Для того, чтобы выбранные опции показывались
правильно, нужно в :doc:`обработчике событий </components/event_handler/event_handlers>` используемого
префикса опций (указанного в ``optprefix``; в данной статье это ``option-prefix``) переписать метод
:doc:`/events/lists/set_custom_query`. Сутью переписывания метода является добавления фильтра по выбранным
и доступным опциям:

.. code:: php

   /**
    * Applies edit picker filters
    *
    * @param kEvent $event
    */
   function SetCustomQuery(&$event)
   {
       $edit_picker_helper =& $this->Application->recallObject('EditPickerHelper');
       /* @var $edit_picker_helper EditPickerHelper */

       $edit_picker_helper->applyFilter($event, 'OptionId');
   }

После выполнения выше указанных действий всё должно корректно заработать. Правда для хранения данных в связанной
таблице (каждое выбранное значение будет отдельной записью) требуется дополнительная настройка, описанная ниже.

Хранение данных в связанной таблице
-----------------------------------

У связанной :doc:`таблицы </database/table_structure>` должен быть свой
:doc:`конфигурационный файл </components/unit_configs/config_files>` и
:doc:`обработчик событий </components/event_handler/event_handlers>`, так как она должна быть
:ref:`подчинённым префиксом <uc_SubItems>` относительно главного. В данной статье главный
:ref:`префикс <uc_Prefix>` это ``sample-prefix``.

Создать конфигурационный файл подчинённого префикса, в котором кроме связки его с главным префиксом
прописать :doc:`hook </components/unit_configs/hooks>`, который будет сохранять выбранные данные.

.. code:: php

   $config = Array (
       'Prefix' => 'sample-prefix-child',
       'Hooks' => Array (
           Array (
               'Mode' => hAFTER,
               'Conditional' => false,
               'HookToPrefix' => '#PARENT#',
               'HookToSpecial' => '*',
               'HookToEvent' => Array('OnAfterItemCreate', 'OnAfterItemUpdate'),
               'DoPrefix' => '',
               'DoSpecial' => '*',
               'DoEvent' => 'OnSaveChildren',
           ),
       ),

       'ForeignKey' => 'ParentId',
       'ParentTableKey' => 'ParentId',
       'ParentPrefix' => 'parent',
       'AutoDelete' => true,
       'AutoClone' => true,

       'Fields' => Array (
           'ChildId' => Array ('type' => 'int', 'not_null' => 1, 'default' => 0),
           'ParentId' => Array ('type' => 'int', 'not_null' => 1, 'required' => 1, 'default' => 0),
           'OptionId' => Array ('type' => 'int', 'not_null' => 1, 'required' => 1, 'default' => 0),
       ),
   );

В :doc:`обработчике событий </components/event_handler/event_handlers>` подчинённого префикса прописать
тело :doc:`hook </components/unit_configs/hooks>`:

.. code:: php

   /**
    * [HOOK] Saves changes from edit picker
    *
    * @param kEvent $event
    */
   function OnSaveChildren(&$event)
   {
       $edit_picker_helper =& $this->Application->recallObject('EditPickerHelper');
       /* @var $edit_picker_helper EditPickerHelper */

       $edit_picker_helper->SaveValues($event, 'OptionField', 'OptionId');
   }

В конфигурационном файле главного префикса нужно прописать его связку с подчинённым префиксом:

.. code:: php

   $config = Array (
       'SubItems' => Array('sample-prefix-child'),
   );

Добавить в :doc:`обработчик событий </components/event_handler/event_handlers>` главного префикса загрузку
значений в блок ``inp_edit_picker`` из подчинённой таблицы:

.. code:: php

   /**
    * Loads edit picker data
    *
    * @param kEvent $event
    */
   function OnAfterItemLoad(&$event)
   {
       parent::OnAfterItemLoad($event);

       $edit_picker_helper =& $this->Application->recallObject('EditPickerHelper');
       /* @var $edit_picker_helper EditPickerHelper */

       $edit_picker_helper->LoadValues($event, 'OptionId', 'sample-prefix-child.OptionId');
   }

В :doc:`обработчике тегов </themes_and_templates/working_with_templates>` (``TagProcessor``) переписать
метод :doc:`/tags/prepare_list_element_params`, который будет использоваться для вывода данных (из тэга
:doc:`/tags/print_list`) из связанной таблицы в списке главного префикса:

.. code:: php

   function PrepareListElementParams(&$object, &$block_params)
   {
       $edit_picker_helper =& $this->Application->recallObject('EditPickerHelper');
       /* @var $edit_picker_helper EditPickerHelper */

       $event = new kEvent($object->getPrefixSpecial() . ':OnAfterItemLoad');
       $edit_picker_helper->LoadValues($event, 'OptionField', 'sample-prefix-child.OptionId');
   }

После этого, для каждой записи в списке, выбранные в поле ``OptionField`` опции будут выводиться через запятую.

Фильтрация в списке
-------------------

На данный момент нету стандартного фильтра, который будет корректно осуществлять фильтрацию данных по
связанной :doc:`таблице </database/table_structure>`. Из-за этого надо будет переписать класс ``kSearchHelper``,
который зарегистрирован в :doc:`фабрике классов </components/unit_configs/class_registration>` под
pseudo ``SearchHelper``.

Для начала нужно создать класс наследник:

.. code:: php

   class ESearchHelper extends kSearchHelper {

       function getCustomFilterSearchClause(&$object, $field_name, $filter_type, $field_options)
       {
           if ($field_name == 'OptionField' && $filter_type == 'options') {
               extract( $this->getFieldInformation($object, $field_name) );
               $field_value = strlen($field_options['submit_value']) ? $this->Conn->qstr($field_options['submit_value']) : false;
               if ($field_value) {
                   $sub_sql = 'SELECT children.ParentId
                               FROM ' . $this->Application->getUnitOption('sample-prefix-child', 'TableName') . ' children
                               WHERE children.OptionId = ' . $field_value;
                   $filter_value = $object->TableName . '.' . $object->IDField . ' IN (' . $sub_sql . ')';
               }

               $field_options['sql_filter_type'] = $sql_filter_type;
               $field_options['value'] = $filter_value;

               return $field_options;
           }

           return parent::getCustomFilterSearchClause($object, $field_name, $filter_type, $field_options);
       }
   }

Файл будет называться ``e_search_helper.php`` (согласно
:doc:`правилу назначения имён </addons/coding_standards/naming_conventions>`) и находиться
в директории ``custom/units/sections``.

Потом нужно зарегистрировать новый класс в фабрике классов:

.. code:: php

   $config = Array (
       'RegisterClasses' => Array (
           Array ('pseudo' => 'SearchHelper', 'class' => 'ESearchHelper', 'file' => 'e_search_helper.php'),
       ),
   );

.. seealso::

   - :doc:`/admin_console_ui/forms/minputhelper_class`

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0_%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%BE%D0%BC_EditPickerHelper
