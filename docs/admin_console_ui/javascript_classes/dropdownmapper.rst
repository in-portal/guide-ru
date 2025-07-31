DropDownMapper
==============
`Data Source`_

В статье о ``JavaScript`` классе
:doc:`AjaxDropdownPreloader </admin_console_ui/javascript_classes/ajaxdropdownpreloader>`, рассматривалось
взаимодействие между двумя **выпадающих меню** (далее **ВМ**):

- первое ВМ - главное;
- второе ВМ - зависимое.

По мере необходимости возможно подключить любое количество зависимых ВМ, причем каждое новое зависимое ВМ
означает создание нового объекта класса
:doc:`AjaxDropdownPreloader </admin_console_ui/javascript_classes/ajaxdropdownpreloader>`. Сложность кода
будет расти и логика становиться менее прозрачной. В результате выгода от использования ``AjaxDropdownPreloader``
становится спорной.

Класс ``AjaxDropdownPreloader`` является оптимальным решением только в случае использования с двумя ВМ
(главным - зависимым). А рассматриваемый в данной статье ``JavaScript`` класс ``DropDownMapper`` специально создан
для реализации связи между тремя и более ВМ. Класс ``DropDownMapper`` реализует связь между множеством ВМ,
используя массив экземпляров класса ``AjaxDropdownPreloader``.

Параметры инициализации
-----------------------

Для успешной реализации связи между многими ВМ необходимо создать экземпляр класса ``DropDownMapper``, передав
ему параметры, описанные в приведённой ниже таблице.

+----------------------+-------------------------------------------------------------------------------------------------------+
| название             | описание                                                                                              |
+======================+=======================================================================================================+
| .. config-property:: | Данный параметр представляет из себя ``JavaScript`` объект, который определяет связь между            |
|    :name: map        | ВМ. Сам объект в свою очередь может состоять из объектов следующего вида:                             |
|    :type: object     |                                                                                                       |
|                      | .. code:: javascript                                                                                  |
|                      |                                                                                                       |
|                      |    'UniqueKey' : {                                                                                    |
|                      |        'Field' : 'FieldName',                                                                         |
|                      |        'Pass' : [<field_names>],                                                                      |
|                      |        'Value' : 'SelectedValue',                                                                     |
|                      |        'Dependent' : false,                                                                           |
|                      |        'SubNodes' : { }                                                                               |
|                      |    }                                                                                                  |
|                      |                                                                                                       |
|                      | - **Field** *(string)* - название поля, при изменении значения в котором будут обновлены              |
|                      |   значения ВМ, указанных в ключе ``SubNodes``;                                                        |
|                      | - **Dependent** *(boolean)* - необязательный параметр, указывающий на то, что данное поле             |
|                      |   является главным и не от кого не зависит; задаётся только для самого первого поля в                 |
|                      |   объекте в ``false``; отсутствие данного ключа приравнивается к его заданию со значением             |
|                      |   ``true``;                                                                                           |
|                      | - **Pass** *(array)* - необязательный параметр, в котором можно указать названия дополнительных       |
|                      |   полей, значения которых нужно передать в запрос на получение новых опций для данного поля;          |
|                      | - **Value** *(mixed)* - необязательный параметр, в котором можно указать то значение, которое         |
|                      |   всегда должно выбираться в этом ВМ после подгрузки в него опций;                                    |
|                      | - **SubNodes** *(object)* - ``JavaScript`` объект, содержащий список ``JavaScript`` объектов,         |
|                      |   зависимых от данного поля (вложенность не ограничена); структура каждого из объектов идентична      |
|                      |   структуре приведённой выше;                                                                         |
|                      |                                                                                                       |
|                      | .. note::                                                                                             |
|                      |                                                                                                       |
|                      |    Названия ключам, используемым для идентификации объектов полей можно давать любые, главное,        |
|                      |    чтобы они были уникальными в пределах своего уровня вложенности.                                   |
+----------------------+-------------------------------------------------------------------------------------------------------+
| .. config-property:: | Ссылка, при заходе на которую будет возвращён                                                         |
|    :name: request    | :doc:`XML документ </application_structure/helper_classes/xml_document_handling>`, содержащий         |
|    :type: string     | новый набор опций для зависимого ВМ. XML документ должен быть в следующем формате:                    |
|                      |                                                                                                       |
|                      | .. code:: xml                                                                                         |
|                      |                                                                                                       |
|                      |    <field_options>                                                                                    |
|                      |        <option>ID1</option>                                                                           |
|                      |        <option>ID2</option>                                                                           |
|                      |    </field_options>                                                                                   |
|                      |                                                                                                       |
|                      | Стоит обратить особое внимание на то, что XML документ содержит только ``ID`` опций (без текста,      |
|                      | который будет виден в зависимом ВМ). Для того, чтобы у опций был и текст нужно изначально заполнить   |
|                      | зависимый ВМ всеми возможными опциями. Обычно установка :ref:`fmt_class_kOptionsFormatter` форматера  |
|                      | на это поле является вполне достаточным.                                                              |
+----------------------+-------------------------------------------------------------------------------------------------------+
| .. config-property:: | Маска для получения любого элемента ввода на форме. Обычно маска получается путём вызова тэга         |
|    :name: input_mask | :doc:`/tags/input_name` со значением ``#FIELD_NAME#`` в качестве названия поля объекта:               |
|    :type: string     |                                                                                                       |
|                      | .. code:: html                                                                                        |
|                      |                                                                                                       |
|                      |    <inp2:prefix_InputName field="#FIELD_NAME#"/>                                                      |
|                      |    // вернёт строку вида: prefix[ID][#FIELD_NAME#]                                                    |
+----------------------+-------------------------------------------------------------------------------------------------------+

Настройка шаблона редактирования
--------------------------------

Для подключения класса ``DropDownMapper`` на форму достаточно получить его экземпляр с правильно переданными
параметрами, в одном из которых и нужно определить зависимость между множеством ВМ. Для примера рассматривается
ситуация, в которой ВМ от полей ``Field_11`` и ``Field_12`` зависят от значения поля ``Field_1``, а
ВМ ``Field_111`` зависит от значения поля ``Field_11``.

После выполнения приведённых ниже шагов настройку шаблона можно считать завершённой.

- Добавить на форме элементы ВМ:

.. code:: html

   <inp2:m_RenderElement name="inp_edit_options" prefix="sample-prefix" field="Field_1" title="la_fld_Field_1"/>
   <inp2:m_RenderElement name="inp_edit_options" prefix="sample-prefix" field="Field_11" title="la_fld_Field_11"/>
   <inp2:m_RenderElement name="inp_edit_options" prefix="sample-prefix" field="Field_12" title="la_fld_Field_12"/>
   <inp2:m_RenderElement name="inp_edit_options" prefix="sample-prefix" field="Field_111" title="la_fld_Field_111"/>

- Добавить вызов класса ``DropDownMapper`` передав ему все требуемые параметры:

.. code:: javascript

   var $mapping = {
       'Level_1' : {
           'Field' : 'Field_1',
           'Dependent' : false,
           'SubNodes' : {
               'Level_11' : {
                   'Field' : 'Field_11',
                   'SubNodes' : {
                       'Level_111' : { 'Field' : 'Field_111' }
                   }
               },

               'Level_12' : {
                   'Field' : 'Field_12'
               }
           }
       }
   };

   new DropDownMapper(
       $mapping,
       '<inp2:m_Link template="dummy" pass="m,sample-prefix" sample-prefix_event="OnGetDropDownXML" q="#QUESTIONED#" f="#FILTERS#" no_amp="1"/>',
       '<inp2:sample-prefix_InputName field="#FIELD_NAME#"/>'
   );

Настройка обработчика событий
-----------------------------

В метод ``OnGetDropDownXML`` необходимо добавить функциональность для получения опций ВМ каждого конкретного случая:

.. code:: php

   /**
    * [AJAX] Метод для получения отфильтрованных опций в виде XML документа.
    *
    * @param kEvent $event
    */
   function OnGetDropDownXML(&$event)
   {
       $event->status = erSTOP;

       if ($this->Application->GetVar('ajax') != 'yes') {
           return ;
       }

       // $q поле соответствующие зависимому ВМ, для которого в данный момент вычисляются опции.
       $q = $this->Application->GetVar('q');

       $f = $this->Application->GetVar('f');
       parse_str($f, $filters);
       // $filters массив, где ключи это поля соответствующих ВМ, а значения выбранные опции из соответствующих ВМ

       // Все необходимые фильтры для SQL запроса в массиве $filters
       // Ниже требуется составить SQL для каждого конкретного случая
       switch ($q) {
           case 'Field_12':
               $sql = 'SELECT ...
                       FROM ...
                       WHERE ...';
               break;

           case 'Field_11':
               $sql = 'SELECT ...
                       FROM ...
                       WHERE ...';
               break;

           case 'Field_111':
               $sql = 'SELECT ...
                       FROM ...
                       WHERE ...';
               break;
       }

       if (!$sql) {
           return ;
       }

       $data = $this->Conn->Query($sql);


       if (!$data) {
           return ;
       }

       $o = '';
       foreach ($data as $row) {
           $attributes = '';
           foreach ($row as $field => $value) {
               if ($field == 'Value' || $field == 'Name') {
                   continue;
               }

               $attributes .= $field . '="' . htmlspecialchars($value) . '" ';
           }

           $o .= '<option value="' . htmlspecialchars($row['Value']) . '" ' . $attributes  .'><![CDATA['  . $row['Name'] . ']]></option>';
       }

       $this->Application->XMLHeader();
       echo '<field_options>' . $o . '</field_options>';
   }

Событие ``OnGetDropDownXML`` необходимо добавить в метод :doc:`mapPermissions </components/using_permissions>`,
который обеспечит проверку наличия у пользователя необходимых прав доступа для вызова данного события:

.. code:: php

   /**
    * Метод связывающий события и права, необходимые для их выполнения.
    *
    */
   function mapPermissions()
   {
       parent::mapPermissions();
       $permissions = Array (
           'OnGetDropDownXML' => Array ('self' => true),
       );

       $this->permMapping = array_merge($this->permMapping, $permissions);
   }

.. tip::

   Также следует обратить внимание на некоторые, описанные ниже, приёмы, которые использовались при
   написании события ``OnGetDropDownXML``.

- В начале события рекомендуется установить статус его выполнения в :ref:`const_erSTOP`. Это укажет
  на то, что по окончания выполнения события не нужно показывать содержание переданного шаблона (в
  данном случае это ``dummy``):

.. code:: php

   $event->status = erSTOP;

- В начале события написать код, который позволит игнорировать запросы, которые будут делать поисковые системы:

.. code:: php

   if ($this->Application->GetVar('ajax') != 'yes') {
       return ;
   }

Параметр ``ajax`` добавляется автоматически при отправлении каждого
:doc:`AJAX </admin_console_ui/forms/ajax_requests>` запроса. Если поисковая система где-то найдёт ссылку, в
которой указано данное событие, то зайдя на неё тело события выполнено не будет.

- Перед выводом :doc:`XML документа </application_structure/helper_classes/xml_document_handling>` на экран
  необходимо послать браузеру соответствующий заголовок. Сделать это можно при помощи метода
  ``Application::XMLHeader``:

.. code:: php

   $this->Application->XMLHeader();


.. seealso::

   - :doc:`/admin_console_ui/javascript_classes/ajaxdropdownpreloader`

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:DropDownMapper
