Site Configs
************
`Data Source`_
`Confluence`_

.. note::

   .. versionadded:: 5.0.0

Функциональность "Site Configs" является упрощённым вариантом использования события
:doc:`/events/general/on_after_config_read` и доступна для всех
:doc:`конфигурационных файлов </components/unit_configs/config_files>` (префиксов) в
системе. Для использования данной функциональности не требуется создавать или
:doc:`регистрировать </components/unit_configs/class_registration>` новые классы
или :doc:`hooks </components/unit_configs/hooks>`.

Расположение файлов
===================
На данный момент все ``site configs`` располагаются в директории ``admin/system_presets``.
Каждый из файлов, находящихся в этой директории влияет только на один, связанный с ним,
:doc:`конфигурационный файл </components/unit_configs/config_files>`. Для того, чтобы создать
новый ``site config`` нужно знать название конфигурационного файла, на который требуется повлиять
и :ref:`префикс <uc_prefix>`, который в нём указан.

Например, если конфигурационный файл называется ``categories_config.php`` и в нём объявлен префикс ``c``,
то файл, содержащий ``site config`` должен называться ``categories_c.php`` (убираем из названия
конфигурационного файла ``_config.php`` и добавляем к нему ``_<prefix>.php``).

Формат файлов
=============
В каждом ``site config`` допускается объявлять глобальные переменные из перечисленного ниже списка.
В результате обработки каждой из этих переменных будет изменена одна или более опция из конфигурационного
файла, с которым этот ``site config`` связан.

+--------------------------------------+------------------------------------------------------------------------------------------------+
| название                             | описание                                                                                       |
+======================================+================================================================================================+
| .. config-property::                 | В данной переменной перечисляются названия тех секций в дереве административной консоли,       |
|    :name: $remove_sections           | которые требуется спрятать от пользователя.                                                    |
|    :type: array                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $remove_sections = Array (                                                                  |
|                                      |        'in-portal:configure_categories',                                                       |
|                                      |        'in-portal:configuration_custom',                                                       |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются названия тех секций в дереве административной консоли,       |
|    :name: $debug_only_sections       | которые требуется показывать только тогда, когда включён |debugger_link| (``debug mode``).     |
|    :type: array                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $debug_only_sections = Array (                                                              |
|                                      |        'in-portal:email_events',                                                               |
|                                      |        'in-portal:phrases',                                                                    |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются названия кнопок на панели инструментов, которые              |
|    :name: $remove_buttons            | нужно спрятать. Кнопки указываются отдельно для каждого требуемого                             |
|    :type: array                      | :doc:`title preset </components/unit_configs/titlepresets_option>`.                            |
|                                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $remove_buttons = Array (                                                                   |
|                                      |        'email_log_list' => Array ('view'),                                                     |
|                                      |        'catalog' => Array ('up', 'home'),                                                      |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те :ref:`физические поля <uc_Fields>`, которые нужно         |
|    :name: $hidden_fields             | спрятать с формы редактирования, связанной с данным ``site config``.                           |
|    :type: array                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $hidden_fields = Array (                                                                    |
|                                      |        'EmailLogId', 'FromUser', 'AddressTo',                                                  |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те :ref:`виртуальные поля <uc_VirtualFields>`, которые       |
|    :name: $virtual_hidden_fields     | нужно спрятать с формы редактирования, связанной с данным ``site config``.                     |
|    :type: array                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $virtual_hidden_fields = Array (                                                            |
|                                      |        'ThumbPath', 'FullUrl',                                                                 |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те :ref:`физические поля <uc_Fields>`, которые нужно         |
|    :name: $debug_only_fields         | показывать на форме редактирования, связанной с данным ``site config`` только тогда,           |
|    :type: array                      | когда включён |debugger_link| (``debug mode``).                                                |
|                                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $debug_only_fields = Array (                                                                |
|                                      |        'EmailLogId', 'FromUser', 'AddressTo',                                                  |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те :ref:`виртуальные поля <uc_VirtualFields>`, которые       |
|    :name: $debug_only_virtual_fields | нужно показывать на форме редактирования, связанной с данным ``site config`` только тогда,     |
|    :type: array                      | когда включён |debugger_link| (``debug mode``).                                                |
|                                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $debug_only_virtual_fields = Array (                                                        |
|                                      |        'ThumbPath', 'FullUrl',                                                                 |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те :ref:`физические поля <uc_Fields>`, которые               |
|    :name: $required_fields           | являются обязательными к заполнению на форме редактирования, связанной с данным                |
|    :type: array                      | ``site config``.                                                                               |
|                                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $required_fields = Array (                                                                  |
|                                      |        'EmailLogId', 'Subject',                                                                |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те :ref:`виртуальные поля <uc_VirtualFields>`,               |
|    :name: $virtual_required_fields   | которые являются обязательными к заполнению на форме редактирования, связанной                 |
|    :type: array                      | с данным ``site config``.                                                                      |
|                                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $virtual_required_fields = Array (                                                          |
|                                      |        'ThumbUrl', 'ThumbPath',                                                                |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те вкладки, которые нужно спрятать на форме редактирования,  |
|    :name: $hide_edit_tabs            | связанной с данным ``site config``. Вкладки указываются отдельно для каждого требуемого        |
|    :type: array                      | набора вкладок.                                                                                |
|                                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $hide_edit_tabs = Array (                                                                   |
|                                      |        'Default' => Array ('general', 'groups'),                                               |
|                                      |        'RegularUsers' => Array ('groups'),                                                     |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+
| .. config-property::                 | В данной переменной перечисляются те поля, которые нужно спрятать из набора колонок,           |
|    :name: $hide_columns              | показываемых в списке записей связанных с данным ``site config``. Поля указываются             |
|    :type: array                      | отдельно для каждого требуемого списка.                                                        |
|                                      |                                                                                                |
|                                      | .. code:: php                                                                                  |
|                                      |                                                                                                |
|                                      |    $hide_columns = Array (                                                                     |
|                                      |        'Default' => Array ('Тimestamp', 'Еvent'),                                              |
|                                      |    );                                                                                          |
+--------------------------------------+------------------------------------------------------------------------------------------------+

Стандартный набор ``site configs`` доступен в архиве: ``core/install/site_configs.zip`` и обновляется при каждом релизе.


.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:Site_Configs
.. _Confluence: http://community.in-portal.org/display/DocRu/1.3.+Site+Configs

.. |debugger_link| replace:: :doc:`режим отладки </application_debugging/debugger>`
