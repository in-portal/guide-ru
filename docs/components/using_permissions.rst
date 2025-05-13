Использование прав доступа
**************************
`Data Source`_

Для разделения прав доступа в К4 применяются **права доступа (permissions)**. В данной статье описаны основные
концепции системы прав доступа, принципы работы с ней и области её применения.

Зачем нужны права доступа?
==========================

На заре существования K4 глобальная система разделения доступа отсутствовала, а для отдельных случаев, при
необходимости, писалась простая, специфичная для конкретного `проекта <K4:Projects>`__ система. Была система
управления правами для ``In-Portal``, работающая только для отдельных ``items``. А в целом система оставалась
легко поддающейся взлому. Стоило только знать названия некоторых :doc:`событий </event_description>` и принцип
построения `имён полей на форме <TagProcessor:InputName>`__.

Но прогресс не стоит на месте, и со временем стало очевидно, что K4 нуждается в стандартизированной системе
управления :doc:`правами доступа </database/table_structure/permissions>`. После долгих и бурных обсуждений
была разработана и внедрена концепция универсальной системы разделения прав доступа. Теперь
`проекты <K4:Projects>`__, построенные на K4, являются гораздо менее уязвимыми в плане безопасности, есть
стандартные механизмы для реализации различных ролей администрирования конкретной системой, и самое
главное - всё это требует минимального вмешательства программиста в процессе разработки.

Работа с правами доступа
========================

Задание списка прав в unit config
---------------------------------

Самое первое, что следует сделать для начала работы с правами - задать в
:doc:`unit config </components/unit_configs/configuration_files>` следующие ключи:

- :ref:`uc_PermSection` - ключ первого уровня, в значении которого нужно задать массив с
  указаниями секций, на которые будут проверяться права доступа. У каждого элемента массива ключ означает тип
  секции, а значение её название. В платформе повсеместно используется только тип секции ``main``, а другие другие
  типы секций (``search``, ``email``, ``custom``) используются только в ``In-Portal``. Начинается название
  :doc:`секции </administrative_console_interface/working_with_templates_and_blocks/adding_sections_in_tree>`
  проверки прав доступа (как и собственно всех секций, определённых в модуле ``custom``) с названия модуля и
  двоеточия, например ``custom:``.
- :ref:`permissions <tree_section_permissions>` - ключ в массиве задания
  :doc:`секции </administrative_console_interface/working_with_templates_and_blocks/adding_sections_in_tree>`.
  Определяет список прав, связанных с данным :doc:`unit config </components/unit_configs/configuration_files>`.
  Обычно содержит стандартные виды прав (``view``, ``add``, ``edit``, ``delete``), а также может содержать
  индивидуальные права (начинаются с ``advanced:``).

Следующая выдержка из :doc:`unit config </components/unit_configs/configuration_files>` демонстрирует объявление
данных ключей:

.. code:: php

   'PermSection' => Array ('main' => 'custom:phones'),

   'Sections' => Array (
       'custom:phones' => Array (
           'parent'        =>  'custom',
           'icon'          =>  'custom:phones',
           'label'         =>  'la_tab_Phones',
           'url'           =>  Array('t' => 'custom/phones/phone_list', 'pass' => 'm'),
           'permissions'       =>  Array('view', 'add', 'edit', 'delete', 'advanced:change_price', 'advanced:edit_phone_sale_info'),
           'priority'      =>  1,
           'type'          =>  stTREE,
       ),
   ),

Назначение прав пользователям
-----------------------------

.. figure:: /images/Group_permissions.gif
   :figwidth: 180px
   :width: 180px
   :align: right
   :alt: Форма редактирования прав доступа группы

   Форма редактирования прав доступа группы

:doc:`Права доступа </database/table_structure/permissions>` в К4 распределяются с помощью
:doc:`групп пользователей </database/table_structure/portal_group>`. Каждый
:doc:`пользователь системы </database/table_structure/portal_user>` назначается в одну или несколько
:doc:`групп </database/table_structure/user_group>`. В свою очередь для каждой группы возможно задать
собственный набор прав, которыми состоящие в ней пользователи будут обладать. В платформе данная возможность
присутствует только при включённой конфигурационной переменной
:ref:`AdvancedUserManagement <cfg_AdvancedUserManagement>` (находится в секции
``Configuration -> System Configuration``). Для редактирования доступных прав группы пользователя следует открыть
редактирование выбранной группы пользователей (в секции ``User Management -> Groups``) и перейти на вкладку
``Permissions``. Описанная выше форма изображена справа.

Каждая строка формы соответствует
:doc:`секции в дереве </administrative_console_interface/working_with_templates_and_blocks/adding_sections_in_tree>`.
В качестве вспомогательной информации при включенном :doc:`DEBUG_MODE </application_debugging/debugger>` под
именем каждой секции в квадратных скобках отображается её название, под которым она была объявлена в
:doc:`unit config </components/unit_configs/configuration_files>`, а также :ref:`префикс <uc_Prefix>` данного
``unit config``. В форме отображаются стандартные права доступа. При нажатии на ссылку ``Change`` в столбце
``Additional`` открывается форма редактирования расширенных прав доступа (тех, чьи названия начинаются с ``advanced:``):

.. figure:: /images/Advanced_permissions.gif
   :figwidth: 180px
   :width: 180px
   :align: left
   :alt: Редактирование расширенных прав доступа группы

   Редактирование расширенных прав доступа группы

Отмечая галочками соответствующие права, они назначаются всем пользователям группы. Если пользователь состоит в
более чем одной группе, и хотя бы в одной из них доступно определённое право доступа, то оно также доступно и ему
(т.е. принцип: "запрещено всё, что не разрешено").

Для редактирование прав, не относящихся ни к одной конкретной секции, используется самая главная (корневая) секция.

.. clear-float::

Делегирование прав доступа
--------------------------

Если требуется, чтобы для конкретного :ref:`префикса <uc_Prefix>` права доступа определялись правами, назначенными
другому префиксу, следует использовать ключ :ref:`SectionPrefix <uc_SectionPrefix>`. Данный ключ задаётся на
верхнем уровне :doc:`unit config </components/unit_configs/configuration_files>`. В случае, когда он присутствует,
ключ :ref:`PermSection <uc_PermSection>` задавать не нужно, т.к. соответствующая
:doc:`секция </administrative_console_interface/working_with_templates_and_blocks/adding_sections_in_tree>` будет
определяться по :ref:`префиксу <uc_Prefix>`, указанному в ключе :ref:`uc_SectionPrefix`.

Использование прав доступа
==========================

Связывание прав и событий
-------------------------

Права доступа проверяются также для запуске :doc:`событий </event_description>` (``events``), инициированных по данным
запроса к серверу (например, если в запросе присутствует переменная вида ``prefix_event``). Чтобы связать событие с
правом(-ами) доступа, используется метод ``kDBEventHandler::mapPermissions()``. В данном методе объявляется массив,
определяющий права доступа для :doc:`событий </event_description>`.

.. code:: php

   function mapPermissions()
   {
       parent::mapPermissions();
       $permissions = Array (
           'OnViewPhone' => Array ('self' => 'view', 'subitem' => 'view'),
           'OnGetPhoneCatalog' => Array ('self' => true),
           'OnModifyPhoneInfo' => Array ('self' => 'edit', 'subitem' => 'add|edit'),
           'OnChangePrice' => Array ('self' => 'advanced:change_price'),
       );

       $this->permMapping = array_merge($this->permMapping, $permissions);
   }

При проверке прав доступа для события массив ``kDBEventHandler::permMapping`` обрабатывается по следующим правилам:

- находится ключ с именем события у :doc:`обработчика событий </event_description>`, объявленного в
  :doc:`unit config </components/unit_configs/configuration_files>` у :ref:`префикса <uc_Prefix>`, для которого
  :doc:`событие </event_description>` вызывается;
- если данный :ref:`префикс <uc_Prefix>` является :doc:`главным </components/working_with_sub_prefixes>`
  (в конкретном случае, так как один и тот же префикс может быть и
  :doc:`главным, и подчинённым </components/working_with_sub_prefixes>` в разных ситуациях), то получается значение
  элемента с ключом ``self``;
- если :ref:`префикс <uc_Prefix>` является :doc:`подчинённым </components/working_with_sub_prefixes>`, то
  получается значение ключа ``subitem``;
- полученное право доступа проверяется всё время у **самого главного** :ref:`префикса <uc_Prefix>`;
- если в полученном значение имеется несколько названий прав доступа, разделённых символом ``|``, то для получения
  доступа пользователю необходимо иметь по крайней мере одно из указанных прав;
- если в результате получается значение ``true``, проверка прав доступа не производится и событие всегда получает
  доступ;
- если в результате получается значение ``false``, проверка прав доступа не производится и событие никогда не
  получает доступ (на практике не используется).

.. warning::

   В вышеупомянутом массиве должны присутствовать связки для каждого события, вызываемого по данным запроса к серверу!
   Если таковых не будет найдено, то попытка вызова события закончится сообщением об ошибке.

Дополнительные проверки прав доступа
------------------------------------

Также дополнительно осуществляются приведённые ниже проверки.

- Только для пользовательской части сайта из события :doc:`/event_description/general_purpose_events/on_item_build`
  вызывается проверка ``view`` права (т.е. права на просмотр данных). Данная проверка происходит только тогда, когда в
  запросе, полученном сервером присутствует ``ID`` объекта и объект пытается использовать его для
  :doc:`получения данных </application_structure/system_classes/working_with_kdbitem_class>` из
  :doc:`базы данных </database/working_with_the_database>`.

- В некоторых событиях, изменяющих данные в базе данных (:doc:`/event_description/events_for_editing_records/on_delete`,
  :doc:`/event_description/events_for_list_operations/on_mass_delete`,
  :doc:`/event_description/events_in_temporary_tables/on_save`,
  :doc:`/event_description/events_for_list_operations/on_mass_clone`,
  :doc:`/event_description/events_for_list_operations/on_mass_approve`,
  :doc:`/event_description/events_for_list_operations/on_mass_decline`,
  :doc:`/event_description/events_for_list_operations/on_mass_move_up`,
  :doc:`/event_description/events_for_list_operations/on_mass_move_down`) проверяется право ``SYSTEM_ACCESS.READONLY``.
  В случае, когда это право установлено, то :doc:`пользователь </database/table_structure/portal_user>` не может
  изменять никакие данные в системе.

Проверка прав доступа из PHP-кода
---------------------------------

Система прав доступа имеет возможность проверки прав из произвольного места PHP-кода (напр.
:doc:`событий </event_description>` или :doc:`тэгов </themes_and_templates/working_with_templates>`). Для вызова
проверки права доступа из PHP-кода следует использовать конструкцию следующего вида:

.. code:: php

   if ($this->Application->CheckPermission('custom:phones.advanced:change_price')) {
       $object->SetField('Price', $new_price);
   }
   else {
       $object->SetError('Price', 'cannot_change_price', 'la_error_YouDontHavePermissionToChangePrice');
   }

Метод ``kApplication::CheckPermission`` имеет следующие параметры:

+-------------------------+----------------------------------------------------------------------------------------------------------------+
| параметр                | описание                                                                                                       |
+=========================+================================================================================================================+
| .. config-property::    | Название :doc:`права доступа </database/table_structure/permissions>`, которое будет проверяется.              |
|    :name: $name         | Название права доступа состоит из 2 частей:                                                                    |
|    :type: string        |                                                                                                                |
|    :ref_prefix: app_cp_ | - название                                                                                                     |
|                         |   :doc:`секции </administrative_console_interface/working_with_templates_and_blocks/adding_sections_in_tree>`  |
|                         |   (напр. ``custom:phones``);                                                                                   |
|                         | - название вида права, которое будет проверяться (напр. ``edit`` или ``advanced:change_price``).               |
|                         |                                                                                                                |
|                         | В названии права название секции отделяется от вида права при помощи символа точки ``.``, напр.                |
|                         | ``custom:phones.advanced:change_price``.                                                                       |
+-------------------------+----------------------------------------------------------------------------------------------------------------+
| .. config-property::    | Тип. Может принимать значение ``1`` (системное право) или ``0`` (право на категорию), по умолчанию             |
|    :name: $type         | принимает значение ``1``.                                                                                      |
|    :type: int           |                                                                                                                |
|    :ref_prefix: app_cp_ |                                                                                                                |
+-------------------------+----------------------------------------------------------------------------------------------------------------+
| .. config-property::    | :ref:`ID категории <tc_Category_CategoryId>`, для которой нужно проверить                                      |
|    :name: $cat_id       | :doc:`право доступа </database/table_structure/permissions>`; имеет смысл передавать только в случае,          |
|    :type: int           | когда значение параметра :ref:`app_cp_$type` равно ``0``.                                                      |
|    :ref_prefix: app_cp_ |                                                                                                                |
+-------------------------+----------------------------------------------------------------------------------------------------------------+

.. note::

   Если :doc:`секция </administrative_console_interface/working_with_templates_and_blocks/adding_sections_in_tree>` в
   названии :doc:`права доступа </database/table_structure/permissions>` совпадает с секцией
   :ref:`префикса <uc_Prefix>`, от которого произошло событие, то для получения названия секции нужно использовать
   метод ``kEvent:getSection`` (т.е. следующий код в :doc:`событии </event_description>` ``$event->getSection();``.

Индивидуальная проверка
-----------------------

Для того, чтобы проверить :doc:`права доступа </database/table_structure/permissions>` на выполнение
:doc:`события </event_description>` нестандартным способом требуется переписать метод
``kDBEventHandler::CheckPermission`` (главное в переписанном методе не забыть вызвать родительской метод).
Следует обратить особое внимание на то, что данный метод вызывается до выполнения запрашиваемого пользователем
:doc:`события </event_description>` и объект, участвующий в событии ещё не инициализирован данными запроса к
серверу. Также следует помнить о том, что в практике переписывание методов проверки прав доступа действительно
нужно очень редко, и большинство проблем можно решить, используя стандартные механизмы.

Проверка прав доступа из шаблонов
---------------------------------

Также предусмотрена возможность проверки прав доступа в шаблонах используя тэг ``m_CheckPermission``:

.. code:: html

   <inp2:m_if check="m_CheckPermission" permissions="custom:phones.advanced:change_price" system="1">
       <inp2:m_RenderElement name="inp_edit_box" prefix="request" field="Price" title="la_fld_Price"/>
   <inp2:m_else />
       <inp2:m_RenderElement name="inp_label" prefix="request" field="Price" title="la_fld_Price"/>
   </inp2:m_if>

Тэгу ``m_CheckPermission`` передаются следующие параметры:

+-------------------------+----------------------------------------------------------------------------------+
| название                | описание                                                                         |
+=========================+==================================================================================+
| .. config-property::    | Название :doc:`события </event_description>`, наличие                            |
|    :name: perm_event    | :doc:`права </database/table_structure/permissions>` вызова которого             |
|    :type: string        | требуется проверить. Событие задаётся в форме ``prefix_special:EventName``,      |
|    :ref_prefix: tag_cp_ | напр. ``phone:OnChangePrice``.                                                   |
+-------------------------+----------------------------------------------------------------------------------+
| .. config-property::    | :ref:`Префикс <uc_Prefix>` объекта, чья основная (primary)                       |
|    :name: perm_prefix   | :doc:`категория </database/table_structure/category>` должна использоваться      |
|    :type: string        | в процессе проверки :doc:`прав доступа </database/table_structure/permissions>`. |
|    :ref_prefix: tag_cp_ | Если требуется явно указать :ref:`ID категории <tc_Category_CategoryId>`,        |
|                         | это можно сделать используя параметр :ref:`tag_cp_cat_id`.                       |
+-------------------------+----------------------------------------------------------------------------------+
| .. config-property::    | Названия :doc:`прав доступа </database/table_structure/permissions>`, наличие    |
|    :name: permissions   | которых нужно проверить. Права можно разбивать на группы, в таком случае:        |
|    :type: string        |                                                                                  |
|    :ref_prefix: tag_cp_ | - права в пределах одной группы проверяются по ``AND`` принципу;                 |
|                         | - права между группами проверяются по ``OR`` принципу.                           |
|                         |                                                                                  |
|                         | Для объединения прав в группу используется запятая (``,``). Для объединения      |
|                         | групп используется вертикальная черта (``|``). Это будет легче понять на         |
|                         | следующем примере:                                                               |
|                         |                                                                                  |
|                         | ============= ================================                                   |
|                         | строка        результат                                                          |
|                         | ============= ================================                                   |
|                         | ``А,B|C,D,E`` ``(А AND B) OR (C AND D AND E)``                                   |
|                         | ``A,B``       ``A AND B``                                                        |
|                         | ``A|B,E``     ``A OR (B AND E)``                                                 |
|                         | ``A|B|D``     ``A OR B OR D``                                                    |
|                         | ============= ================================                                   |
+-------------------------+----------------------------------------------------------------------------------+
| .. config-property::    | Указывает на то, что проверяемые права являются системными, т.е. не зависят      |
|    :name: system        | от текущей :doc:`категории </database/table_structure/category>`.                |
|    :type: int           |                                                                                  |
|    :ref_prefix: tag_cp_ | .. note::                                                                        |
|                         |                                                                                  |
|                         |    По умолчанию проверяются не системные права.                                  |
+-------------------------+----------------------------------------------------------------------------------+
| .. config-property::    | :ref:`ID категории <tc_Category_CategoryId>`, для которой нужно проверить        |
|    :name: cat_id        | :doc:`право доступа </database/table_structure/permissions>`. Имеет смысл        |
|    :type: int           | передавать только в случае, когда значение параметра :ref:`tag_cp_system`        |
|    :ref_prefix: tag_cp_ | равно ``0``, либо параметр ``system` не передан.                                 |
+-------------------------+----------------------------------------------------------------------------------+

Примеры использования тэга ``m_CheckPermission``:

.. code:: html

   <inp2:m_if check="m_CheckPermission" permissions="custom:phones.advanced:change_price|custom:phones.view" system="1">...
   <!-- разрешено ли хотя бы одно из прав custom:phones.advanced:change_price и custom:phones.view -->

   <inp2:m_if check="m_CheckPermission" permissions="custom:phones.advanced:change_price,custom:phones.view" system="1">...
   <!-- разрешены ли оба права -->

   <inp2:m_if check="m_CheckPermission" permissions="custom:phones.advanced:change_price,custom:phones.view|custom:phones.edit" system="1">...
   <!-- разрешены ли одновременно права custom:phones.advanced:change_price и custom:phones.view, или разрешено ли право custom:phones.edit -->

   <inp2:m_if check="m_CheckPermission" permissions="custom:phones.advanced:change_price">...
   <!-- разрешено ли право custom:phones.advanced:change_price в текущей категории (не передан параметр system) -->

   <inp2:m_if check="m_CheckPermission" permissions="custom:phones.advanced:change_price" perm_prefix="product">...
   <!-- разрешено ли право custom:phones.advanced:change_price в текущей категории;
   текущую категорию определить по тому, в какой категории находится текущий объект с prefix'ом product -->

   <inp2:m_if check="m_CheckPermission" permissions="custom:phones.advanced:change_price" cat_id="5">...
   <!-- разрешено ли право custom:phones.advanced:change_price в категории c id=5 -->

   <inp2:m_if check="m_CheckPermission" perm_event="phone:OnChangePrice">...
   <!-- разрешен ли запуск события OnChangePrice для prefix'a phone  -->

Системные права и права категорий
=================================

.. figure:: /images/Category-permissions.jpg
   :figwidth: 180px
   :width: 180px
   :align: right
   :alt: Форма редактирования прав доступа для категории

   Форма редактирования прав доступа для категории

.. container:: float-fixer

   В K4 реализовано два типа прав доступа:

   - **системные права** - задаются глобально, определяют право вне зависимости от
     :doc:`категории </database/table_structure/category>` в которой находиться
     :doc:`пользователь </database/table_structure/portal_user>`, используются чаще;
   - **права категорий** - задаются отдельно для каждой :doc:`категории </database/table_structure/category>`,
     проверяются, исходя из текущей :doc:`категории </database/table_structure/category>`; актуально
     для ``In-Portal``'a.

   Права :doc:`категории </database/table_structure/category>` можно назначить, открыв редактирование категории и
   перейдя на закладку ``Permissions``. Затем, выбрав группу пользователей в верхней части и модуль в нижней,
   можно задать соответствующие :doc:`права доступа </database/table_structure/permissions>`. Галочка в колонке
   ``Access`` определяет наличие права. При отметке галочки ``Inherited`` право наследуется у :ref:`родительской
   категории <tc_Category_ParentId>`, а в колонке ``Inherited From`` выведена категория, с которой будет
   наследовано право в случае отметки галочки ``Inherited``. Данная форма доступна только в ``In-Portal``'e.

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:%D0%98%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%BF%D1%80%D0%B0%D0%B2_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0

.. include:: /includes/broken_links.rst

.. Broken Links:
   =============
   K4:Projects
   TagProcessor:InputName
