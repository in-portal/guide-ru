Работа с опцией TitlePresets
============================
`Data Source`_
`Eng Data Source`_

Практически на каждой странице `сайта <K4:Projects>`__ присутствует такой элемент как
:doc:`заголовок </admin_console_ui/templates_and_blocks/combined_header_block>`
(``title``). Это текст, в краткой форме поясняющий что за информация отображается на странице. В заголовке может
быть просто текст, переводимая в зависимости от выбранного :doc:`языка </database/table_structure/language>`
интерфейса :doc:`фраза </database/table_structure/phrase>`, а также информация о данных, отображаемых на странице.
Например, если на странице отображаются данные :doc:`пользователя </database/table_structure/portal_user>`,
то в заголовке уместно показать :ref:`имя этого пользователя <tc_PortalUser_Login>`. Если на странице имеется
список :doc:`заказов </database/table_structure/orders>`, то в заголовке можно показать количество заказов.

Итак, заголовок страницы можно составить из небольшого количества типичных элементов. Это позволяет
практически во всех случаях использовать стандартный способ для формирования заголовка страницы и таким
стандартным способом в K4 является настройка заголовков посредством задания опции :ref:`uc_TitlePresets`
в :doc:`unit Configs </components/unit_configs/config_files>` и последующего вывода на странице стандартным
блоком |combined_header_link|. Этот блок содержит тэг :doc:`/tags/section_title`, который собирает элементы
заголовка в строку и показывает её в стандартном, именно для этого предназначенном месте дизайна.

Поскольку тэг :doc:`/tags/section_title` в блоке |combined_header_link| вызывается с параметром
``pass_params="true"``, то через блок |combined_header_link| можно задать любые параметры для тага
:doc:`/tags/section_title`, кроме ``cut_first``, который уже задан внутри этого блока.

Настройка
---------

.. code:: php

   'TitlePresets' => Array (
       'title_preset_name' => Array (
           'new_status_labels' => Array (),
           'edit_status_labels' => Array (),
           'new_titlefield' => Array (),

           'prefixes' => Array (),
           'tag_params' => Array (),
           'format' => '',
       )
   )

В приведённом выше примере отображены ключи первого уровня, записанные в обобщённой форме. Там имеется только один
заголовок ``title_preset_name``. Заголовков может быть сколь угодно много но, естественно, каждый из них должен
иметь уникальный ключ в массиве :ref:`uc_TitlePresets`. Желательно в качестве ключа выбирать строку, соответствующую
по смыслу страницам, на которых заголовок будет показываться. Например

- ``user_edit`` - для шаблона редактирования :doc:`пользователей </database/table_structure/portal_user>`;
- ``denied_order_list`` - для списка отклонённых :doc:`заказов </database/table_structure/orders>`.

Ключи настройки
^^^^^^^^^^^^^^^

+------------------------------+-------------------------------------------------------------------------------------------------+
| название                     | описание                                                                                        |
+==============================+=================================================================================================+
| .. config-property::         | В данном ключе для **каждого**, используемого в заголовке,                                      |
|    :name: new_status_labels  | :ref:`префикса <uc_Prefix>` задаётся текст, обозначающий, что происходит создание               |
|    :type: array              | новой записи. Данный текст (обычно это фраза вида ``!la_title_AddingOrder!``) в                 |
|    :ref_prefix: tpo_         | последствии будет вставлен вместо кода ``#prefix_status#`` в значении ключа                     |
|                              | :ref:`tpo_format`, но только когда происходит создание новой записи в                           |
|                              | :doc:`базе данных </database/using_database>`. Это подробнее показано на приведённом            |
|                              | ниже примере.                                                                                   |
|                              |                                                                                                 |
|                              | .. code:: php                                                                                   |
|                              |                                                                                                 |
|                              |    'order_edit' => Array (                                                                      |
|                              |        'new_status_labels' => Array ('ord' => '!la_title_AddingOrder!'),                        |
|                              |        'prefixes' => Array ('ord'), 'format' => '#ord_status#'),                                |
|                              |    ),                                                                                           |
|                              |                                                                                                 |
|                              | .. note::                                                                                       |
|                              |                                                                                                 |
|                              |    Данный ключ обычно используется вместе с ключами :ref:`tpo_edit_status_labels`               |
|                              |    и :ref:`tpo_new_titlefield` (только в In-Portal) для получения полноценных форм              |
|                              |    создания и редактирования записей.                                                           |
+------------------------------+-------------------------------------------------------------------------------------------------+
| .. config-property::         | В данном ключе для **каждого**, используемого в заголовке, :ref:`префикса <uc_Prefix>`          |
|    :name: edit_status_labels | задаётся текст, обозначающий, что происходит редактирование созданной ранее записи.             |
|    :type: array              | Данный текст (обычно это фраза вида ``!la_title_EditingOrder!``) в последствии будет            |
|    :ref_prefix: tpo_         | вставлен вместо кода ``#prefix_status#`` в значении ключа :ref:`tpo_format`, но                 |
|                              | только когда происходит редактирование созданной ранее записи в                                 |
|                              | :doc:`базе данных </database/using_database>`. Это подробнее показано на приведённом            |
|                              | ниже примере.                                                                                   |
|                              |                                                                                                 |
|                              | .. code:: php                                                                                   |
|                              |                                                                                                 |
|                              |    'order_edit' => Array (                                                                      |
|                              |        'edit_status_labels' => Array ('ord' => '!la_title_EditingOrder!'),                      |
|                              |        'prefixes' => Array ('ord'), 'format' => '#ord_status#'),                                |
|                              |    ),                                                                                           |
|                              |                                                                                                 |
|                              | .. note::                                                                                       |
|                              |                                                                                                 |
|                              |    Данный ключ обычно используется вместе с ключами :ref:`tpo_new_status_labels` и              |
|                              |    :ref:`tpo_new_titlefield` (только в In-Portal) для получения полноценных форм                |
|                              |    создания и редактирования записей.                                                           |
+------------------------------+-------------------------------------------------------------------------------------------------+
| .. config-property::         | В данном ключе для **каждого**, используемого в заголовке, :ref:`префикса <uc_Prefix>`          |
|    :name: new_titlefield     | задаётся текст, показываемый **вместо пустого значения** поля, указанного в опции               |
|    :type: array              | :ref:`uc_TitleField`. Данный текст (обычно это фраза вида ``!la_title_NewOrder!``) в            |
|    :ref_prefix: tpo_         | последствии будет вставлен вместо кода ``#prefix_titlefield#`` в значении ключа                 |
|                              | :ref:`tpo_format`, но только когда происходит создание новой записи в                           |
|                              | :doc:`базе данных </database/using_database>`. Это подробнее показано на приведённом            |
|                              | ниже примере.                                                                                   |
|                              |                                                                                                 |
|                              | .. code:: php                                                                                   |
|                              |                                                                                                 |
|                              |    'order_edit' => Array (                                                                      |
|                              |        'new_titlefield' => Array ('ord' => '!la_title_NewOrder!'),                              |
|                              |        'prefixes' => Array ('ord'), 'format' => '#ord_titlefield#'),                            |
|                              |    ),                                                                                           |
|                              |                                                                                                 |
|                              | .. note::                                                                                       |
|                              |                                                                                                 |
|                              |    Данный ключ в In-Portal обычно используется вместе с ключами :ref:`tpo_new_status_labels`    |
|                              |    и :ref:`tpo_edit_status_labels` для получения полноценных форм создания и редактирования     |
|                              |    записей.                                                                                     |
+------------------------------+-------------------------------------------------------------------------------------------------+
| .. config-property::         | В данном ключе задаётся список :ref:`префиксов <uc_Prefix>`, используемых для вывода            |
|    :name: prefixes           | заголовка. При этом префиксы для объектов типа ``Item`` пишутся как есть, а к                   |
|    :type: array              | :ref:`префиксам <uc_Prefix>` объектов типа ``List`` дописывается слово ``_List``.               |
|    :ref_prefix: tpo_         | Например так задаются префиксы для одного :doc:`заказа </database/table_structure/orders>`      |
|                              | и для списка архива заказов если выходит что они оба нужны в одном заголовке:                   |
|                              |                                                                                                 |
|                              | .. code:: php                                                                                   |
|                              |                                                                                                 |
|                              |    'prefixes' => Array ('ord', 'ord.archived_List')                                             |
+------------------------------+-------------------------------------------------------------------------------------------------+
| .. config-property::         | В этом необязательном ключе можно задать параметры инициализации для **каждого** из объектов,   |
|    :name: tag_params         | использующихся в заголовке. Инициализация объектов происходит в момент первого обращения к      |
|    :type: array              | ним из метода ``kApplication::recallObject``. Этот метод в качестве третьего параметра          |
|    :ref_prefix: tpo_         | принимает массив параметров инициализации ``$event_params``. Данный ключ как раз и предусмотрен |
|                              | для того, чтобы эти параметры можно было задать. Например, чтобы изменить (``override``)        |
|                              | прописанное по умолчанию количество записей, показываемых на одной странице списка, для         |
|                              | :ref:`префикса <uc_Prefix>` этого списка можно задать параметр ``per_page``:                    |
|                              |                                                                                                 |
|                              | .. code:: php                                                                                   |
|                              |                                                                                                 |
|                              |    'prefixes' => Array ('conf'),                                                                |
|                              |    'tag_params' => Array (                                                                      |
|                              |        'conf' => Array (                                                                        |
|                              |            'per_page' => -1                                                                     |
|                              |        ),                                                                                       |
|                              |    ),                                                                                           |
|                              |                                                                                                 |
|                              | .. note::                                                                                       |
|                              |                                                                                                 |
|                              |    Стоит отдельно подчеркнуть, что в ключе ``tag_params`` существует по ассоциативному массиву  |
|                              |    на **каждый** :ref:`префикс <uc_Prefix>`, которому они нужны.                                |
+------------------------------+-------------------------------------------------------------------------------------------------+
| .. config-property::         | Это главный ключ, представляющий из себя строку, из которой получается итоговый заголовок на    |
|    :name: format             | странице после замены всех специальных элементов на их значения. Эта строка может содержать:    |
|    :type: string             |                                                                                                 |
|    :ref_prefix: tpo_         | - просто текст;                                                                                 |
|                              | - фразы;                                                                                        |
|                              | - информацию об объектах типа ``Item``, использующихся на странице;                             |
|                              |                                                                                                 |
|                              |   - статус объекта - создание или редактирование;                                               |
|                              |   - значение поля, настроенного как заголовочное (:ref:`uc_TitleField`);                        |
|                              |   - значение любого поля;                                                                       |
|                              |                                                                                                 |
|                              | - информацию об объектах типа ``List``, использующихся на странице;                             |
|                              |                                                                                                 |
|                              |   - количество записей с фильтрами и без оных.                                                  |
|                              |                                                                                                 |
|                              | Простой текст в итоге отображается как есть. :doc:`Фразы </database/table_structure/phrase>`    |
|                              | - заменяются на их перевод. Фразы должны экранироваться с помощью восклицательных знаков,       |
|                              | например ``!la_title_OrderShipping!``. Прочие элементы экранируются знаком ``#``, например      |
|                              | ``#ord.denied_recordcount#``.                                                                   |
+------------------------------+-------------------------------------------------------------------------------------------------+
| .. config-property::         | .. versionadded:: 5.0.0                                                                         |
|    :name: toolbar_buttons    |                                                                                                 |
|    :type: array              | В этом ключе перечисляются названия (без модуля, т.е. ``sample_button``, а не                   |
|    :ref_prefix: tpo_         | ``custom:sample_button``) тех кнопок на панели инструментов, которые возможно будет             |
|                              | в последствии прятать через :doc:`Site Configs </system_setup/site_configs>`                    |
|                              | функциональность. Это будет показано на ниже приведённом примере.                               |
|                              |                                                                                                 |
|                              | .. code:: php                                                                                   |
|                              |                                                                                                 |
|                              |    'toolbar_buttons' => Array ('new_item', 'edit', 'delete', 'view'),                           |
+------------------------------+-------------------------------------------------------------------------------------------------+


Особые возможности ключа "format"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------+--------------------------------------------------------------------------------------------------+
| название                           | описание                                                                                         |
+====================================+==================================================================================================+
| ``#prefix[.special]_status#``      | Данный код заменится на текст, заданный в массиве ключа :ref:`tpo_new_status_labels`,            |
|                                    | если объект находится в статусе "новый" (его ``ID <= 0``) и на текст, заданный в                 |
|                                    | массиве ключа :ref:`tpo_edit_status_labels` во всех остальных случаях. Эти ключи                 |
|                                    | задаются с указанием :ref:`префиксов <uc_Prefix>` в качестве ключей подмассива:                  |
|                                    |                                                                                                  |
|                                    | .. code:: php                                                                                    |
|                                    |                                                                                                  |
|                                    |    'new_status_labels' => Array ('ord' => '!la_title_AddingOrder!'),                             |
|                                    |    'edit_status_labels' => Array ('ord' => '!la_title_EditingOrder!'),                           |
|                                    |    'prefixes' => Array ('ord'), 'format' => '#ord_status#'),                                     |
+------------------------------------+--------------------------------------------------------------------------------------------------+
| ``#prefix[.special]_titlefield#``  | Данный код замениться на значение поля, определённого в конфигурации соответствующего            |
|                                    | префикса как :ref:`uc_TitleField`. Подробнее это будет видно на ниже приведённом                 |
|                                    | примере.                                                                                         |
|                                    |                                                                                                  |
|                                    | .. code:: php                                                                                    |
|                                    |                                                                                                  |
|                                    |    'prefixes' => Array ('ord'), 'format' => "#ord_titlefield#' - !la_title_General!",            |
|                                    |                                                                                                  |
|                                    | В результате выполнения выше приведённого примера в заголовке будет показано значение            |
|                                    | поля, заданного в ключе :ref:`uc_TitleField` у префикса                                          |
|                                    | :doc:`ord </database/table_structure/orders>`, то есть, поле :ref:`tc_Orders_OrderNumber`        |
|                                    | от текущего заказа.                                                                              |
|                                    |                                                                                                  |
|                                    | Может случиться, что открыт шаблон создания записи, и поле, заданное в ключе                     |
|                                    | :ref:`uc_TitleField` у префикса имеет пустое значение. Для того, чтобы и в этом случае           |
|                                    | заголовок страницы выглядел содержательным, можно настроить ключ :ref:`tpo_new_titlefield`.      |
|                                    | Таким образом обеспечивается что код вида ``#prefix[.special]_titlefield#`` никогда не           |
|                                    | превратится в пустоту. Подробнее это будет видно на ниже приведённом примере.                    |
|                                    |                                                                                                  |
|                                    | .. code:: php                                                                                    |
|                                    |                                                                                                  |
|                                    |    'new_titlefield' => Array ('ord' => '!la_title_NewOrder!')                                    |
+------------------------------------+--------------------------------------------------------------------------------------------------+
| ``#prefix[.special]_<FieldName>#`` | Также присутствует возможность вывести значение любого поля объекта указав его следующим         |
|                                    | образом: ``#prefix[.special]_FieldName#``. В ниже приведённом примере будет отображено           |
|                                    | значение поля :ref:`tc_Orders_OrderNumber` текущего заказа.                                      |
|                                    |                                                                                                  |
|                                    | .. code:: php                                                                                    |
|                                    |                                                                                                  |
|                                    |    'format' => "#ord_status# '#ord_OrderNumber#' - !la_title_General!"                           |
+------------------------------------+--------------------------------------------------------------------------------------------------+
| ``#prefix[.special]_recordcount#`` | Когда для заголовка настроен объект типа ``List``, то в заголовке можно показать количество      |
|                                    | записей. Подробнее это будет видно на ниже приведённом примере.                                  |
|                                    |                                                                                                  |
|                                    | .. code:: php                                                                                    |
|                                    |                                                                                                  |
|                                    |    'prefixes' => Array ('ord.denied_List'),                                                      |
|                                    |    'format' => "!la_title_OrdersDenied! (#ord.denied_recordcount#)"                              |
|                                    |                                                                                                  |
|                                    | Когда в списке нет фильтров, этот код заменится на количество записей. Если же фильтры имеются,  |
|                                    | то код заменится на строку, включающую количество записей с фильтром и количество записей без    |
|                                    | фильтра, например: ``25 of 79``.                                                                 |
+------------------------------------+--------------------------------------------------------------------------------------------------+
| ``#section_label#``                | .. versionadded:: 5.0.0                                                                          |
|                                    |                                                                                                  |
|                                    | Данный код замениться на перевод опции :ref:`tree_section_label` в описании секции, переданной   |
|                                    | в параметре :ref:`element_ch_section` блока                                                      |
|                                    | :doc:`combined_header </admin_console_ui/templates_and_blocks/combined_header_block>`, который   |
|                                    | в итоге и будет показывать ``title preset``. Это будет показано на ниже приведённом примере.     |
|                                    |                                                                                                  |
|                                    | .. code:: php                                                                                    |
|                                    |                                                                                                  |
|                                    |    'format' => "#section_label#"                                                                 |
+------------------------------------+--------------------------------------------------------------------------------------------------+

.. _default_title_preset:

Заголовок "default"
^^^^^^^^^^^^^^^^^^^

Также есть специальный заголовок ``default``, данные которого будут автоматически скопированы в каждый
созданный заголовок. Его можно использовать для конфигурации элементов, повторяющихся в прочих заголовках.
Например, такую конфигурацию, где все заголовки настроены одинаково, кроме ключа :ref:`tpo_format`:

.. code:: php

   'TitlePresets' => Array (
       'order_edit_general' => Array (
           'new_status_labels' => Array ('ord' => '!la_title_AddingOrder!'),
           'edit_status_labels' => Array ('ord' => '!la_title_EditingOrder!'),
           'new_titlefield' => Array ('ord' => '!la_title_NewOrder!'),

           'prefixes' => Array ('ord'), 'format' => "#ord_status# '#ord_titlefield#' - !la_title_General!"
       ),

       'order_edit_billing' => Array (
           'new_status_labels' => Array ('ord' => '!la_title_AddingOrder!'),
           'edit_status_labels' => Array ('ord' => '!la_title_EditingOrder!'),
           'new_titlefield' => Array ('ord' => '!la_title_NewOrder!'),

           'prefixes' => Array ('ord'), 'format' => "#ord_status# '#ord_titlefield#' - !la_title_OrderBilling!",
       ),

       'order_edit_shipping' => Array (
           'new_status_labels' => Array ('ord' => '!la_title_AddingOrder!'),
           'edit_status_labels' => Array ('ord' => '!la_title_EditingOrder!'),
           'new_titlefield' => Array ('ord' => '!la_title_NewOrder!'),

           'prefixes' => Array ('ord'), 'format' => "#ord_status# '#ord_titlefield#' - !la_title_OrderShipping!"
       ),
   ),

можно заменить эквивалентной конфигурацией, убрав повторяющиеся настройки в ключ :ref:`default <default_title_preset>`:

.. code:: php

   'TitlePresets' => Array (
       'default' => Array (
           'new_status_labels' => Array ('ord' => '!la_title_AddingOrder!'),
           'edit_status_labels' => Array ('ord' => '!la_title_EditingOrder!'),
           'new_titlefield' => Array ('ord' => '!la_title_NewOrder!'),

           'prefixes' => Array ('ord'),
       ),

       'orders_edit_general' => Array ('format' => "#ord_status# '#ord_titlefield#' - !la_title_General!"),
       'orders_edit_billing' => Array ('format' => "#ord_status# '#ord_titlefield#' - !la_title_OrderBilling!"),
       'orders_edit_shipping' => Array ('format' => "#ord_status# '#ord_titlefield#' - !la_title_OrderShipping!"),
   ),

Избегая с помощью ключа :ref:`default <default_title_preset>` дублирования кода, облегчаются последующие изменения - изменения
придётся делать только в одном месте.

Примеры использования
---------------------

Заголовки в In-Portal и платформы формируются по одной схеме, но в платформе имеется **3 основных отличия**:

- не используется ключ :ref:`tpo_new_titlefield`;
- не используется конструкция ``#prefix[.special]_recordcount#`` (т.к. её результат уже виден под списком);
- для :doc:`главных префиксов </components/working_with_sub_prefixes>` не задаются заголовки
  (т.к. в них только и показывается количество записей из предыдущего пункта).

Список главного префикса
^^^^^^^^^^^^^^^^^^^^^^^^

Конфигурация:

.. code:: php

   'product_list' => Array ('prefixes' => Array ('p_List'), 'format' => "!la_title_Products! (#p_recordcount#)")

Код в шаблоне:

.. code:: xml

   <inp2:m_RenderElement name="combined_header" prefix="p" section="in-commerce:products" title_preset="product_list"/>

.. note::

   Для платформы заголовок списка главного префикса не задаётся и не используется.

Редактирование главного префикса
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Конфигурация:

.. code:: php

   'default' => Array (
       'new_status_labels' => Array ('p' => '!la_title_AddingProduct!'),
       'edit_status_labels' => Array ('p' => '!la_title_EditingProduct!'),
       'new_titlefield' => Array ('p' => '!la_title_NewProduct!'),
   ),

   'product_edit' => Array ('prefixes' => Array ('p'), 'format' => "#p_status# '#p_titlefield#' - !la_title_General!"),

Код в шаблоне:

.. code:: xml

   <inp2:m_RenderElement name="combined_header" prefix="p" section="in-commerce:products" title_preset="product_edit"/>

.. note::

   Для платформы убирается код, содержащий ``'new_titlefield'``.

Список подчинённого префикса
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Конфигурация:

.. code:: php

   'default' => Array (
       'new_status_labels' => Array ('p' => '!la_title_AddingProduct!'),
       'edit_status_labels' => Array ('p' => '!la_title_EditingProduct!'),
       'new_titlefield' => Array ('p' => '!la_title_NewProduct!'),
   ),

   'image_list' => Array ('prefixes' => Array ('p', 'img_List'), 'format' => "#p_status# '#p_titlefield#' - !la_title_Images! (#img_recordcount#)"),

Код в шаблоне:

.. code:: xml

   <inp2:m_RenderElement name="combined_header" prefix="p" section="in-commerce:products" title_preset="image_list"/>

.. note::

   Для платформы убирается ``(#img_recordcount#)`` (и пробел перед ним) из значения
   ключа :ref:`tpo_format` и код, содержащий ``'new_titlefield'``.

Редактирование подчинённого префикса
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Конфигурация:

.. code:: php

   'default' => Array (
       'new_status_labels' => Array ('p' => '!la_title_AddingProduct!'),
       'edit_status_labels' => Array ('p' => '!la_title_EditingProduct!'),
       'new_titlefield' => Array ('p' => '!la_title_NewProduct!'),
   ),

   'image_edit' => Array (
       'new_status_labels' => Array ('img' => '!la_title_AddingImage!'),
       'edit_status_labels' => Array ('img' => '!la_title_EditingImage!'),
       'new_titlefield' => Array ('img' => '!la_title_NewImage!'),

       'prefixes' => Array ('p', 'img'), 'format' => "#p_status# '#p_titlefield#' - #img_status# '#img_titlefield#'",
   )

Код в шаблоне:

.. code:: xml

   <inp2:m_RenderElement name="combined_header" prefix="p" section="in-commerce:products" title_preset="image_edit"/>

.. note::

   Для платформы убирается код, содержащий ``'new_titlefield'``.

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0_%D1%81_%D0%BE%D0%BF%D1%86%D0%B8%D0%B5%D0%B9_TitlePresets
.. _Eng Data Source: http://guide.in-portal.org/eng/index.php/K4:Using_%22TitlePresets%22_Option

.. include:: /includes/broken_links.rst

.. Broken Links:
   =============
   K4:Projects
   TagProcessor:SectionTitle

.. |combined_header_link| replace:: :doc:`combined_header </admin_console_ui/templates_and_blocks/combined_header_block>`
