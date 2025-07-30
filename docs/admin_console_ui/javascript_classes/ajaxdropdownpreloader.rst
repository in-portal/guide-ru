AjaxDropdownPreloader
=====================
`Data Source`_

Часто на форме редактирования возникает необходимость вывести два **выпадающих меню** (далее **ВМ**), где
набор опций второго ВМ напрямую зависит от выбранной в первом ВМ опции. Причем требуется динамическое
обновление опций зависимого ВМ без отправки (``submit``) формы на сервер. Вышеописанную функциональность
можно самостоятельно реализовать стандартными средствами ``HTML`` и ``Javascript``, однако рекомендуется
использовать уже написанный ``JavaScript`` класс ``AjaxDropdownPreloader``, который её реализует.

При изменении значения в главном ВМ, отсылается :doc:`AJAX </admin_console_ui/forms/ajax_requests>` запрос
на сервер. Сервер выполняет необходимые расчёты и получает новый набор опций для подчиненного ВМ. Полученный
набор опций возвращается в виде :doc:`XML документа </application_structure/helper_classes/xml_document_handling>`
на страницу, которая послала AJAX запрос. Далее происходит обработка полученного XML документа и замена опций
подчиненного ВМ средствами ``JavaScript`` на стороне клиента.

Параметры инициализации
-----------------------

Для успешной реализации связи между двумя ВМ необходимо создать экземпляр класса AjaxDropdownPreloader,
передав ему параметры, описанные в приведённой ниже таблице.

+----------------------------+-------------------------------------------------------------------------------------+
| название                   | описание                                                                            |
+============================+=====================================================================================+
| .. config-property::       | Ссылка, при заходе на которую будет возвращён                                       |
|    :name: $url             | :doc:`XML документ </application_structure/helper_classes/xml_document_handling>`,  |
|    :type: string           | содержащий новый набор опций для зависимого ВМ. XML документ должен быть в          |
|                            | следующем формате:                                                                  |
|                            |                                                                                     |
|                            | .. code:: xml                                                                       |
|                            |                                                                                     |
|                            |    <field_options>                                                                  |
|                            |        <option>ID1</option>                                                         |
|                            |        <option>ID2</option>                                                         |
|                            |    </field_options>                                                                 |
|                            |                                                                                     |
|                            | Стоит обратить особое внимание на то, что XML документ содержит только ID опций     |
|                            | (без текста, который будет виден в зависимом ВМ). Для того, чтобы у опций был и     |
|                            | текст нужно изначально заполнить зависимый ВМ всеми возможными опциями. Обычно      |
|                            | установка :ref:`fmt_class_kOptionsFormatter` форматера на это поле является         |
|                            | вполне достаточным.                                                                 |
+----------------------------+-------------------------------------------------------------------------------------+
| .. config-property::       | Маска для получения любого элемента ввода на форме. Обычно маска получается путём   |
|    :name: $input_mask      | вызова тэга :doc:`/tags/input_name` со значением ``#FIELD#`` в качестве названия    |
|    :type: string           | поля объекта:                                                                       |
|                            |                                                                                     |
|                            | .. code:: html                                                                      |
|                            |                                                                                     |
|                            |    <inp2:prefix_InputName field="#FIELD#"/>                                         |
|                            |    // вернёт строку вида: prefix[ID][#FIELD#]                                       |
+----------------------------+-------------------------------------------------------------------------------------+
| .. config-property::       | Название поля главного ВМ.                                                          |
|    :name: $filter_field    |                                                                                     |
|    :type: string           |                                                                                     |
+----------------------------+-------------------------------------------------------------------------------------+
| .. config-property::       | Название поля подчиненного ВМ.                                                      |
|    :name: $dependend_field |                                                                                     |
|    :type: string           |                                                                                     |
+----------------------------+-------------------------------------------------------------------------------------+
| .. config-property::       | Данный параметр позволяет указать на то, какое значение должно быть выбрано в       |
|    :name: value            | зависимом ВМ после обновления его набора опций. Если его не передать, то            |
|    :type: int              | автоматически будет выбрано значение, которое было выбрано до получения нового      |
|                            | набора опций (только если оно в нём также присутствует).                            |
+----------------------------+-------------------------------------------------------------------------------------+

.. _ajax_dropdown_preloader_template_setup:

Настройка шаблона
-----------------

Для примера рассматривается стандартная форма редактирования с двумя ВМ:

- ``MainField`` - главное ВМ;
- ``DependentField`` - зависимое и ВМ.

При изменении выбранного значения в поле ``MainField`` срабатывает событие ``onchange`` и через него подгружаются
соответствующие опции в поле ``DependentField``. После выполнения приведённых ниже шагов настройку шаблона можно
считать завершенной.

- Добавить элементы ВМ:

.. code:: html

   <inp2:m_RenderElement name="inp_edit_options" prefix="sample-prefix" field="MainField" title="la_fld_MainField"/>
   <inp2:m_RenderElement name="inp_edit_options" prefix="sample-prefix" field="DependentField" title="la_fld_DependentField"/>

- Создать экземпляр класса ``AjaxDropdownPreloader``:

.. code:: javascript

   var DependentFieldPreloader = new AjaxDropdownPreloader(
       '<inp2:m_Link template="dummy" sample-prefix_event="OnQueryDependentXML" pass="m,sample-prefix" filter_value="#FILTER_VALUE#" no_amp="1"/>',
       '<inp2:sample-prefix_InputName field="#FIELD#"/>', 'MainField', 'DependentField'
   );

- Назначить событие ``onchange`` для главного ВМ:

.. code:: javascript

   addEvent(DependentFieldPreloader.getControl('MainField'), 'change', function() {DependentFieldPreloader.Query()});

- Отфильтровать значения для зависимого ВМ сразу после загрузки страницы.

.. code:: javascript

   Application.setHook('m:OnAfterWindowLoad', function () { DependentFieldPreloader.Query(); });

Весь приведённый выше ``JavaScript`` код нужно писать после того, как на форме будут отображены элементы,
с которыми он работает. Самое оптимальное для этого место перед подключением шаблона ``incs/footer``. Это
наглядно будет показано на ниже приведённом примере.

.. code:: html

   <script type="text/javascript">
       // javascript code here
   </script>

   <inp2:m_include t="incs/footer"/>

В данном случае переданный шаблон ``dummy`` использоваться не будет (его даже может не существовать), а вся
подготовка :doc:`XML документа </application_structure/helper_classes/xml_document_handling>` будет
происходить в :doc:`событии </events>` ``OnQueryDependentXML``.

Настройка обработчика событий
-----------------------------

В :doc:`обработчик событий </components/event_handler/event_handlers>` от :ref:`префикса <uc_Prefix>`
``sample-prefix`` необходимо добавить событие ``OnQueryDependentXML`` (указанное на
:ref:`шаблоне редактирования <ajax_dropdown_preloader_template_setup>`), которое в результате своей
работы будет возвращать в поток вывода (output stream)
:doc:`XML документ </application_structure/helper_classes/xml_document_handling>`.  Возвращаемый XML
документ будет в последствии обрабатывается классом ``AjaxDropdownPreloader`` и зависимое ВМ будет
заполняется опциями на стороне клиента. После выполнения всех ниже приведённых шагов можно считать
настройку обработчика событий завершённой.

Добавить тело события ``OnQueryDependentXML`` в
:doc:`обработчик событий </components/event_handler/event_handlers>` от :ref:`префикса <uc_Prefix>`
``sample-prefix``:

.. code:: php

   /**
    * [AJAX] Метод для получения отфильтрованных опций в виде XML документа.
    *
    * @param kEvent $event
    */
   function OnQueryDependentXML(&$event)
   {
       $event->status = erSTOP;

       $filter_value = $this->Application->GetVar('filter_value');
       if (!$filter_value || ($this->Application->GetVar('ajax') != 'yes')) {
           return ;
       }

       $sql = 'SELECT DependentTable.FieldId
           FROM DependentTable
           WHERE DependentTable.MainId = ' . $filter_value;
       $dependent_ids = $this->Conn->GetCol($sql);

       $xml = '';
       foreach ($dependent_ids as $id) {
           $xml .= '<option>' . $id . '</option>';
       }
       $xml = '<field_options>' . $xml . '</field_options>';

       $this->Application->XMLHeader();
       echo $xml;
   }

Событие ``OnQueryDependentXML`` необходимо добавить в метод :doc:`mapPermissions </components/using_permissions>`,
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
           'OnQueryDependentXML' => Array ('self' => 'view'),
       );

       $this->permMapping = array_merge($this->permMapping, $permissions);
   }

.. tip::

   Также следует обратить внимание на некоторые, описанные ниже, приёмы, которые использовались при
   написании события ``OnQueryDependentXML``.

- В начале события рекомендуется установить статус его выполнения в :ref:`const_erSTOP`. Это укажет на
  то, что по окончания выполнения события не нужно показывать содержание переданного шаблона (в данном
  случае это ``dummy``):

.. code:: php

   $event->status = erSTOP;

- В начале события написать код, который позволит игнорировать запросы, которые будут делать
  поисковые системы:

.. code:: php

   if ($this->Application->GetVar('ajax') != 'yes') {
       return ;
   }

Параметр ``ajax`` добавляется автоматически при отправлении каждого
:doc:`AJAX </admin_console_ui/forms/ajax_requests>` запроса. Если поисковая система где-то найдёт ссылку,
в которой указано данное событие, то зайдя на неё тело события выполнено не будет.

- Перед выводом :doc:`XML документа </application_structure/helper_classes/xml_document_handling>` на экран
  необходимо послать браузеру соответствующий заголовок. Сделать это можно при помощи метода
  ``Application::XMLHeader``:

.. code:: php

   $this->Application->XMLHeader();

.. note::

   Конечно такой заголовок слать не нужно, если не планируется возвращать XML документ.

Использование метода AfterProcess
---------------------------------

В классе ``AjaxDropdownPreloader`` также доступен абстрактный метод ``AfterProcess``. Данный метод
рекомендуется переопределять, когда требуется выполнение специфической функциональности после выполнения
фильтраций опций зависимого ВМ.

.. seealso::

   - :doc:`/admin_console_ui/javascript_classes/dropdownmapper`

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:AjaxDropdownPreloader
