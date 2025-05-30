Работа с подчинёнными префиксами
********************************
`Data Source`_

Технология главных и подчинённых префиксах впервые появилась в K4 и призвана упростить создание тесно связанных
между собой сущностей.

Отличия между главными и подчинёнными префиксами
================================================

Подчинённый :ref:`префикс <uc_Prefix>` отличаться от главного тем, что он:

- Не может существовать отдельно без главного.
- У него упрощена структура :doc:`конфигурационного файла </components/unit_configs/config_files>`
  (многое объявлено в главном конфигурационном файле).
- Нет :doc:`секции </admin_console_ui/templates_and_blocks/tree_sections>` в дереве слева.
- Записи подчиненного :ref:`префикса <uc_Prefix>` всегда визуально привязаны к редактированию какой-то записи
  главного префикса.
- При создании/изменении записи в административной консоли вызываются события :doc:`/events/live_editing/on_create`
  и :doc:`/events/live_editing/on_update` вместо события :doc:`/events/onpresave/on_pre_save` (как у главного).

Возможное применение
====================

Технология в силу своего удобства все чаще находит применение в повседневной работе. Ниже приведены несколько
примеров типичного ее применения:

- сущность "город" - главный префикс, сущность "район" - подчиненный префикс;
- сущность "дом" - главный префикс, сущность "изображения дома" - подчиненный префикс.

Более сложный пример, в котором присутствуют несколько уровней зависимости:

- сущность "пользователь" - главный префикс;
- "заказ" (заказы пользователя) - подчиненный префикс;
- "товары в заказе" - подчиненный префикс для сущности "заказ".

.. note::

   Ниже приведён подробно описанный пример написания всех требуемых файлов для демонстрации того, как
   реализовано создание и редактирование главного и подчинённого префиксов.

Создание двух связанных таблиц
==============================

Ниже приведены запросы к базе данных, при помощи которых будут созданы таблицы, содержащие данные о городах
и регионах.

.. code:: sql

   CREATE TABLE int_Cities (
     CityId int(11) NOT NULL AUTO_INCREMENT,
     CityTitle varchar(128) DEFAULT NULL,
     PRIMARY KEY (CityId)
   );

   CREATE TABLE int_CityAreas (
    AreaId int(11) NOT NULL AUTO_INCREMENT,
    CityId int(11) NOT NULL,
    AreaTitle varchar(128) DEFAULT NULL,
    PRIMARY KEY (AreaId),
    KEY CityId (CityId)
   );

Нужно обратить внимание, что в таблице ``int_CityAreas`` создано специальное поле ``CityId`` для связи с
главной таблицей ``int_Cities``. Также поставлен индекс на это поле, что часто забывают делать.

Настройка конфигурационных файлов
=================================

Конфигурационный файл главного префикса
---------------------------------------

- Префикс: ``city``.
- Файл: ``city_config.php``.

.. code:: php

   $config = Array (
       'Prefix' => 'city',
       'ItemClass' => Array ('class' => 'kDBItem', 'file' => '', 'build_event' => 'OnItemBuild'),
       'ListClass' => Array ('class' => 'kDBList', 'file' => '', 'build_event' => 'OnListBuild'),
       'EventHandlerClass' => Array ('class' => 'CityEventHandler', 'file' => 'city_eh.php', 'build_event' => 'OnBuild'),
       'TagProcessorClass' => Array ('class' => 'CityTagProcessor', 'file' => 'city_tp.php', 'build_event' => 'OnBuild'),
       'AutoLoad' => true,

       'QueryString' => Array (
           1 => 'id',
           2 => 'Page',
           3 => 'event',
           4 => 'mode',
       ),

       'IDField' => 'CityId',
       'TableName' => TABLE_PREFIX . 'Cities',
       'SubItems' => Array ('area'),

       'TitlePresets' => Array (
           'default' => Array (
               'new_status_labels' => Array ('city' => '!la_title_Adding_City!'),
               'edit_status_labels' => Array ('city' => '!la_title_Editing_City!'),
           ),

           'city_edit' => Array ('prefixes' => Array ('city'), 'format' => "#city_status# '#city_titlefield#' - !la_title_General!"),
           'city_edit_areas' => Array ('prefixes' => Array ('city', 'area_List'), 'format' => "#city_status# '#city_titlefield#' - !la_title_Areas! (#area_recordcount#)"),

           'city_area_edit' => Array (
               'prefixes' => Array ('city', 'area'),
               'new_status_labels' => Array ('area' => '!la_title_Adding_Area!'),
               'edit_status_labels' => Array ('area' => '!la_title_Editing_Area!'),
               'new_titlefield' => Array ('area' => '!la_title_New_Area!'),
               'format' => "#city_status# '#city_titlefield#' - #area_status# '#area_titlefield#'"
           ),
       ),

       'Sections' => Array (
           'custom:city' => Array (
               'parent' => 'custom',
               'icon' => 'custom:city',
               'label' => 'la_tab_Cities',
               'url' => Array ('t' => 'custom/city/city_list', 'pass' => 'm'),
               'permissions' => Array ('view', 'add', 'edit', 'delete'),
               'priority' => 1,
               'type' => stTREE
           ),
       ),
   );

Особенности данного конфигурационного файла:

- Задание подчиненного префикса ``area`` строкой кода ``'SubItems' => Array('area'),``.
- В ключе массива :doc:`TitlePresets </components/unit_configs/working_with_titlepresets_option>`
  по мимо стандартных секций ``default``, ``city_list``, ``city_edit`` есть еще 2 дополнительные секции,
  которые описывают список районов города ``city_edit_areas`` и форму редактирования района ``city_area_edit``.

Конфигурационный файл подчиненного префикса
-------------------------------------------

- Префикс: ``area``.
- Файл: ``area_config.php``.

.. code:: php

   $config = Array (
       'Prefix' => 'area',
       'ItemClass' => Array ('class' => 'kDBItem', 'file' => '', 'build_event' => 'OnItemBuild'),
       'ListClass' => Array ('class' => 'kDBList', 'file' => '', 'build_event' => 'OnListBuild'),
       'EventHandlerClass' => Array ('class' => 'AreaEventHandler', 'file' => 'area_eh.php', 'build_event' => 'OnBuild'),
       'TagProcessorClass' => Array ('class' => 'AreaTagProcessor', 'file' => 'area_tp.php', 'build_event' => 'OnBuild'),
       'AutoLoad' => true,

       'QueryString' => Array (
           1 => 'id',
           2 => 'Page',
           3 => 'event'
       ),
       'IDField' => 'AreaId',
       'TableName' => TABLE_PREFIX . 'CityAreas',

       'ParentPrefix' => 'city',
       'ForeignKey'  => 'CityId',
       'ParentTableKey' => 'CityId',
       'AutoDelete' => true,
       'AutoClone' => true,

       'Fields' => Array (
           'AreaId' => Array ('type' => 'int', 'not_null' => 1, 'default' => 0),
           'CityId' => Array ('type' => 'int', 'not_null' => 1, 'default' => 0),
           'AreaTitle' => Array (
               'type' => 'string',
               'required' => 1, 'not_null' => 1, 'default' => ''
           ),
       ),
   );

Особенности данного конфигурационного файла:

В разделе ``Fields`` описано поле ``CityId`` для связи с главным префиксом.

.. code:: php

   'CityId' => Array ('type' => 'int', 'not_null' => 1, 'default' => 0),

Ниже будет более подробно рассмотрен фрагмент выше приведённого кода, который устанавливает связь подчиненного
префикса с главным префиксом:

.. code:: php

   'ParentPrefix' => 'city',
   'ForeignKey' => 'CityId',
   'ParentTableKey' => 'CityId',
   'AutoDelete' => true,
   'AutoClone' => true,

+--------------------------+-----------------------------------------------------------------------+
| параметр                 | описание                                                              |
+==========================+=======================================================================+
| .. config-property::     | Название главного префикса.                                           |
|    :name: ParentPrefix   |                                                                       |
|    :type: string         |                                                                       |
+--------------------------+-----------------------------------------------------------------------+
| .. config-property::     | Название cвязующей колонки в таблице от починённого префикса, т.е.    |
|    :name: ForeignKey     | ``inp_CityAreas``.                                                    |
|    :type: string         |                                                                       |
+--------------------------+-----------------------------------------------------------------------+
| .. config-property::     | Название cвязующей колонки в таблице от главного префикса, т.е.       |
|    :name: ParentTableKey | ``inp_Cities``.                                                       |
|    :type: string         |                                                                       |
+--------------------------+-----------------------------------------------------------------------+
| .. config-property::     | Указывает на то, что делать с подчинёнными записями при удалении      |
|    :name: AutoDelete     | главной записи (тоже удалять или оставлять).                          |
|    :type: boolean        |                                                                       |
+--------------------------+-----------------------------------------------------------------------+
| .. config-property::     | Указывает на то, что делать с подчинёнными записями при клонировании  |
|    :name: AutoClone      | главной записи (тоже клонировать или нет).                            |
|    :type: boolean        |                                                                       |
+--------------------------+-----------------------------------------------------------------------+

- Разделы :doc:`TitlePresets </components/unit_configs/working_with_titlepresets_option>`
  и :doc:`Sections </admin_console_ui/templates_and_blocks/tree_sections>`
  не используются для подчинённых префиксов, т.к. они заданы у главного префикса.

Создание шаблонов главного префикса
===================================

Шаблон списка главного префикса
-------------------------------

- Префикс: ``city``.
- Файл: ``city_list.tpl``.

.. code:: xml

   <inp2:m_include t="incs/header"/>
   <inp2:m_RenderElement name="combined_header" section="custom:city" prefix="city" pagination="1"/>

   <!-- ToolBar -->
   <table class="toolbar" height="30" cellspacing="0" cellpadding="0" width="100%" border="0">
       <tr>
           <td>
               <table width="100%" cellpadding="0" cellspacing="0">
                   <tr>
                       <td>
                           <script type="text/javascript">
                               a_toolbar = new ToolBar();

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'new_item',
                                       '<inp2:m_phrase label="la_ToolTip_NewCity" escape="1"/>::<inp2:m_phrase label="la_Add" escape="1"/>',
                                       function() {
                                           std_precreate_item('city', 'custom/city/city_edit');
                                       }
                                   )
                               );

                               function edit()
                               {
                                   std_edit_item('city', 'custom/city/city_edit');
                               }

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'edit',
                                       '<inp2:m_phrase label="la_ToolTip_Edit" escape="1"/>::<inp2:m_phrase label="la_ShortToolTip_Edit" escape="1"/>',
                                       edit
                                   )
                               );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'delete',
                                       '<inp2:m_phrase label="la_ToolTip_Delete" escape="1"/>',
                                       function() {
                                           std_delete_items('city');
                                       }
                                   )
                               );

                               a_toolbar.AddButton( new ToolBarSeparator('sep1') );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'view',
                                       '<inp2:m_phrase label="la_ToolTip_View" escape="1"/>',
                                       function(id) {
                                           show_viewmenu(a_toolbar,'view');
                                       }
                                   )
                               );

                               a_toolbar.Render();
                           </script>
                       </td>

                       <inp2:m_RenderElement name="search_main_toolbar" prefix="city" grid="Default"/>
                   </tr>
               </table>
           </td>
       </tr>
   </table>

   <inp2:m_RenderElement name="grid" PrefixSpecial="city" IdField="CityId" grid="Default" grid_filters="1"/>

   <script type="text/javascript">
       Grids['city'].SetDependantToolbarButtons( new Array('edit', 'delete') );
   </script>

   <inp2:m_include t="incs/footer"/>

Шаблон списка стандартный и не содержит каких-либо особенностей.

Шаблон редактирования главного префикса
---------------------------------------

- Префикс: ``city``.
- Файл: ``city_edit.tpl``.

.. code:: xml

   <inp2:adm_SetPopupSize width="570" height="540"/>
   <inp2:m_include t="incs/header"/>

   <inp2:m_RenderElement name="combined_header" section="custom:city" prefix="city" title_preset="city_edit" tab_preset="Default"/>

   <!-- ToolBar -->
   <table class="toolbar" height="30" cellspacing="0" cellpadding="0" width="100%" border="0">
       <tr>
           <td>
               <script type="text/javascript">
                   a_toolbar = new ToolBar();

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'select',
                           '<inp2:m_phrase label="la_ToolTip_Save" escape="1"/>',
                           function() {
                               submit_event('city','<inp2:city_SaveEvent/>');
                           }
                       )
                   );

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'cancel',
                           '<inp2:m_phrase label="la_ToolTip_Cancel" escape="1"/>',
                           function() {
                               cancel_edit('city','OnCancelEdit','<inp2:city_SaveEvent/>','<inp2:m_Phrase label="la_FormCancelConfirmation" escape="1"/>');
                           }
                       )
                   );

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'reset_edit',
                           '<inp2:m_phrase label="la_ToolTip_Reset" escape="1"/>',
                           function() {
                               reset_form('city', 'OnReset', '<inp2:m_Phrase label="la_FormResetConfirmation" escape="1"/>');
                           }
                       )
                   );

                   a_toolbar.AddButton( new ToolBarSeparator('sep1') );

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'prev',
                           '<inp2:m_phrase label="la_ToolTip_Prev" escape="1"/>',
                           function() {
                               go_to_id('city', '<inp2:city_PrevId/>');
                           }
                       )
                   );

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'next',
                           '<inp2:m_phrase label="la_ToolTip_Next" escape="1"/>',
                           function() {
                               go_to_id('city', '<inp2:city_NextId/>');
                           }
                       )
                   );

                   a_toolbar.Render();

                   <inp2:m_if check="city_IsSingle">
                       a_toolbar.HideButton('prev');
                       a_toolbar.HideButton('next');
                       a_toolbar.HideButton('sep1');
                   <inp2:m_else/>
                       <inp2:m_if check="city_IsLast">
                           a_toolbar.DisableButton('next');
                       </inp2:m_if>
                       <inp2:m_if check="city_IsFirst">
                           a_toolbar.DisableButton('prev');
                       </inp2:m_if>
                   </inp2:m_if>
               </script>
           </td>

           <inp2:m_RenderElement name="ml_selector" prefix="city"/>
       </tr>
   </table>

   <inp2:city_SaveWarning name="grid_save_warning"/>
   <inp2:city_ErrorWarning name="form_error_warning"/>
   <div id="scroll_container">
       <table class="edit-form">
           <inp2:m_RenderElement name="inp_id_label" prefix="city" field="CityId" title="la_fld_Id"/>
           <inp2:m_RenderElement name="inp_edit_box" prefix="city" field="CityTitle" title="la_fld_Title" />
       </table>
   </div>

   <inp2:m_include t="incs/footer"/>

Редактирование раздела "EditTabPresets"
=======================================

Данный раздел нужен для того, чтобы создать вкладки для перехода между формой редактирования города и списком районов,
принадлежащих данному городу.

Для реализации этого нужно:

- В файле ``city_config.php`` описать секцию :ref:`EditTabPresets <combined_header_edit_tab_presets>`:

.. code:: php

   'EditTabPresets' => Array (
       'Default' => Array (
           Array ('title' => 'la_tab_General', 't' => 'custom/city/city_edit', 'priority' => 1),
           Array ('title' => 'la_tab_Areas', 't' => 'custom/city/city_edit_areas', 'priority' => 2),
       ),
   ),

Ключ массива ``Default`` будет названием набора вкладок, которые будут использоваться для перехода между формой
редактирования города и списком его регионов. Подробнее об этом написано
в :ref:`этой статье <combined_header_edit_tab_presets>`.

- На шаблонах ``city_edit.tpl``, ``city_edit_areas.tpl`` нужно передать дополнительный параметр
  :ref:`element_ch_tab_preset` при использовании блока |combined_header| вверху шаблона. Его значение нужно
  установить равным ``Default`` (или то, что было ранее определено). Например использование блока combined_header
  в шаблоне ``city_edit.tpl`` будет выглядеть следующим образом:

.. code:: html

   <inp2:m_RenderElement name="combined_header" prefix="city" section="custom:city" title_preset="city_edit" tab_preset="Default"/>

Создание шаблонов подчинённого префикса
=======================================

Шаблон списка подчинённого префикса
-----------------------------------

- Префикс: ``area``.
- Файл: ``city_edit_areas.tpl``.

.. code:: xml

   <inp2:adm_SetPopupSize width="570" height="540"/>
   <inp2:m_include t="incs/header"/>
   <inp2:m_RenderElement name="combined_header" section="custom:city" prefix="city" title_preset="city_edit_areas" tab_preset="Default" pagination_prefix="area" pagination="1"/>

   <!-- ToolBar -->
   <table class="toolbar" height="30" cellspacing="0" cellpadding="0" width="100%" border="0">
       <tr>
           <td>
               <table width="100%" cellpadding="0" cellspacing="0">
                   <tr>
                       <td>
                           <script type="text/javascript">
                               a_toolbar = new ToolBar();

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'select',
                                       '<inp2:m_phrase label="la_ToolTip_Save" escape="1"/>',
                                       function() {
                                           submit_event('city', '<inp2:city_SaveEvent/>');
                                       }
                                   )
                               );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'cancel',
                                       '<inp2:m_phrase label="la_ToolTip_Cancel" escape="1"/>',
                                       function() {
                                           cancel_edit('city','OnCancelEdit','<inp2:city_SaveEvent/>','<inp2:m_Phrase label="la_FormCancelConfirmation" escape="1"/>');
                                       }
                                   )
                               );

                               a_toolbar.AddButton( new ToolBarSeparator('sep1') );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'prev',
                                       '<inp2:m_phrase label="la_ToolTip_Prev" escape="1"/>',
                                       function() {
                                           go_to_id('city', '<inp2:city_PrevId/>');
                                       }
                                   )
                               );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'next',
                                       '<inp2:m_phrase label="la_ToolTip_Next" escape="1"/>',
                                       function() {
                                           go_to_id('city', '<inp2:city_NextId/>');
                                       }
                                   )
                               );

                               a_toolbar.AddButton( new ToolBarSeparator('sep2') );

                               <!-- Start Area Buttons -->

                               function edit()
                               {
                                   std_edit_temp_item('area', 'custom/city/city_area_edit');
                               }

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'new_item',
                                       '<inp2:m_phrase label="la_ToolTip_New_Area" escape="1"/>',
                                       function() {
                                           std_new_item('area', 'custom/city/city_area_edit')
                                       }
                                   )
                               );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'edit',
                                       '<inp2:m_phrase label="la_ToolTip_Edit" escape="1"/>',
                                       edit
                                   )
                               );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'delete',
                                       '<inp2:m_phrase label="la_ToolTip_Delete" escape="1"/>',
                                       function() {
                                           std_delete_items('area')
                                       }
                                   )
                               );

                               a_toolbar.AddButton(
                                   new ToolBarButton(
                                       'view',
                                       '<inp2:m_phrase label="la_ToolTip_View" escape="1"/>',
                                       function(id) {
                                           show_viewmenu(a_toolbar, 'view');
                                       }
                                   )
                               );

                               <!-- End Area Buttons -->

                               a_toolbar.Render();

                               <inp2:m_if check="city_IsSingle">
                                   a_toolbar.HideButton('prev');
                                   a_toolbar.HideButton('next');
                                   a_toolbar.HideButton('sep1');
                               <inp2:m_else/>
                                   <inp2:m_if check="city_IsLast">
                                       a_toolbar.DisableButton('next');
                                   </inp2:m_if>
                                   <inp2:m_if check="city_IsFirst">
                                       a_toolbar.DisableButton('prev');
                                   </inp2:m_if>
                               </inp2:m_if>
                           </script>
                       </td>
                   </tr>
               </table>
           </td>
       </tr>
   </table>

   <inp2:m_RenderElement name="grid" PrefixSpecial="area" IdField="AreaId" grid="Default"/>
   <script type="text/javascript">
   Grids['area'].SetDependantToolbarButtons( new Array('edit','delete') );
   </script>

   <inp2:m_include t="incs/footer"/>

Данный шаблон создается на основе шаблона для редактирования главного префикса ``city`` (есть все кнопки
формы редактирования) и стандартного списка для подчиненного префикса ``area`` с кнопками для вызова формы
создания, формы редактирования и удаления районов.

Особенности данного файла:

- При вызове блока |combined_header| нужно передать параметры ``title_preset="city_edit_areas"`` и
  ``tab_preset="Default"``:

.. code:: html

   <inp2:m_RenderElement name="combined_header" section="custom:city" prefix="city" title_preset="city_edit_areas" tab_preset="Default" />

Шаблон редактирования подчинённого префикса
-------------------------------------------

- Префикс: ``area``.
- Файл: ``city_area_edit.tpl``.

.. code:: xml

   <inp2:adm_SetPopupSize width="750" height="570"/>
   <inp2:m_include t="incs/header" body_properties="" />
   <inp2:m_RenderElement name="combined_header" prefix="city" section="custom:city" title_preset="city_area_edit"/>

   <!-- ToolBar -->
   <table class="toolbar" height="30" cellspacing="0" cellpadding="0" width="100%" border="0">
       <tr>
           <td>
               <script type="text/javascript">
                   a_toolbar = new ToolBar();

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'select',
                           '<inp2:m_phrase label="la_ToolTip_Save" escape="1"/>',
                           function() {
                               submit_event('area', '<inp2:area_SaveEvent/>');
                           }
                       )
                   );

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'cancel',
                           '<inp2:m_phrase label="la_ToolTip_Cancel" escape="1"/>',
                           function() {
                               cancel_edit('area','OnCancel','<inp2:area_SaveEvent/>','<inp2:m_Phrase label="la_FormCancelConfirmation" escape="1"/>');
                           }
                       )
                   );

                   a_toolbar.AddButton(
                       new ToolBarButton(
                           'reset_edit',
                           '<inp2:m_phrase label="la_ToolTip_Reset" escape="1"/>',
                           function() {
                               reset_form('area', 'OnReset', '<inp2:m_Phrase label="la_FormResetConfirmation" escape="1"/>');
                           }
                       )
                   );

                   a_toolbar.Render();
               </script>
           </td>
       </tr>
   </table>

   <inp2:area_SaveWarning name="grid_save_warning"/>
   <inp2:area_ErrorWarning name="form_error_warning"/>

   <div id="scroll_container">
       <table class="edit-form">
           <inp2:m_RenderElement name="inp_edit_hidden" prefix="area" field="CityId"/>
           <inp2:m_RenderElement name="inp_id_label" prefix="area" field="AreaId" title="la_fld_Id"/>
           <inp2:m_RenderElement name="inp_edit_box" prefix="area" field="Title" title="la_fld_Title" />
       </table>
   </div>

   <inp2:m_include t="incs/footer"/>

Особенности данного файла:

- При вызове блока |combined_header| нужно передать параметр ``title_preset="city_area_edit"``.

.. code:: html

   <inp2:m_RenderElement name="combined_header" prefix="city" section="custom:city" title_preset="city_area_edit"/>

- Через скрытое поле формы объявлено поле ``CityId``, в которое
  записывается ``Id`` текущего города.

.. code:: html

   <inp2:m_RenderElement name="inp_edit_hidden" prefix="area" field="CityId"/>

Вкладки на форме редактирования подчинённого префикса
=====================================================

В случае, когда на форме редактирования починённого :ref:`префикса <uc_Prefix>` требуется использование вкладок
необходимо проделать следующие дополнительные действия.

Обработчик событий главного префикса
------------------------------------

- Префикс: ``city``.
- Файл: ``city_eh.php``.

В :doc:`обработчике событий </events>` главного префикса требуется переписать событие
:doc:`/events/onpresave/on_pre_save_and_go_to_tab` так, чтобы при наличии ``ID`` подчинённого префикса в
запросе от сервера оно автоматически передавалось дальше при переходе между вкладками. Если этого не
сделать, то автоматически будет передаваться только ``ID`` главного префикса, т.к. именно у него, при
хождении по вкладкам, вызывается событие :doc:`/events/onpresave/on_pre_save_and_go_to_tab`.

.. code:: php

   /**
    * Saves edited item in temp table and goes
    * to passed tabs, by redirecting to it with OnPreSave event
    *
    * @param kEvent $event
    */
   function OnPreSaveAndGoToTab(&$event)
   {
       $event->CallSubEvent('OnPreSave');
       if ($event->status == erSUCCESS) {
           $area_id = $this->Application->GetVar('area_id');
           if (is_numeric($area_id)) {
               $event->SetRedirectParam('area_id', $area_id);
           }

           $event->redirect = $this->Application->GetVar($event->getPrefixSpecial(true) . '_GoTab');
       }
   }

Конфигурационный файл главного префикса (2)
-------------------------------------------

- Префикс: ``city``.
- Файл: ``city_config.php``.

Набор вкладок (ключ
:doc:`EditTabPresets </admin_console_ui/templates_and_blocks/combined_header_block>`),
который будет использоваться на форме редактирования подчинённого префикса нужно будет определить
в :doc:`unit config </components/unit_configs/config_files>` главного префикса (т.е. также как
и ключ :doc:`TitlePresets </components/unit_configs/working_with_titlepresets_option>`).

.. code:: php

   'EditTabPresets' => Array (
       'AreaEdit' => Array (
           Array ('title' => 'la_tab_General', 't' => 'custom/city/area_edit', 'priority' => 1),
           Array ('title' => 'la_tab_Additional', 't' => 'custom/city/area_edit_additional', 'priority' => 2),
       ),
   );

Конфигурационный файл подчиненного префикса (2)
-----------------------------------------------

- Префикс: ``area``.
- Файл: ``area_config.php``.

В конфигурационном файле подчинённого префикса нужно добавить :doc:`hook </components/unit_configs/hooks>`,
который при наличии данных подчинённого префикса в момент выполнения события :doc:`/events/onpresave/on_pre_save`
у главного префикса будет их также сохранять.

.. attention::

   .. versionadded:: 4.3.2

   Было добавлено :doc:`/events/onpresave/on_pre_save_sub_item` событие.

.. code:: php

   'Hooks' => Array (
       Array (
           'Mode' => hAFTER,
           'Conditional' => true,
           'HookToPrefix' => '#PARENT#',
           'HookToSpecial' => '*',
           'HookToEvent' => Array ('OnPreSave'),
           'DoPrefix' => '',
           'DoSpecial' => '*',
           'DoEvent' => 'OnPreSaveSubItem',
       ),
   ),

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0_%D1%81_%D0%BF%D0%BE%D0%B4%D1%87%D0%B8%D0%BD%D1%91%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_%D0%BF%D1%80%D0%B5%D1%84%D0%B8%D0%BA%D1%81%D0%B0%D0%BC%D0%B8

.. |combined_header| replace:: :doc:`combined_header </admin_console_ui/templates_and_blocks/combined_header_block>`
