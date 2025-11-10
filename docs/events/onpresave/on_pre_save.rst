OnPreSave
=========
`Data Source`_

.. include:: /includes/not_finished.rst

Событие сохраняет запись редактируемого объекта во временную таблицу. В случае, если Id объекта не передан,
событие создаёт запись во временной таблице.

Вызывается из шаблонов
----------------------

- ``kernel\admin_templates\categories\categories_edit_permissions.tpl``
- ``in-commerce\admin_templates\shipping\shipping_costs.tpl``
- ``in-commerce\admin_templates\orders\orders_edit_billing.tpl``

Вызывается из событий
---------------------

- ``TranslatorEventHandler::OnSaveAndClose``
- ``TranslatorEventHandler::OnChangeLanguage``
- :doc:`/events/temp_editing/on_save`
- :doc:`/events/onpresave/on_pre_save_and_go`
- :doc:`/events/onpresave/on_pre_save_and_go_to_tab`
- :doc:`/events/onpresave/on_pre_save_popup`
- :doc:`/events/onpresave/on_pre_save_and_open_translator`
- :doc:`/events/onpresave/on_pre_save_and_change_language`
- ``CurrenciesEventHandler::OnUpdateRate``
- ``OrdersEventHandler::OnQuietPreSave``
- ``ProductsEventHandler::OnPreSaveAndGo``
- ``ProductsEventHandler::OnPreSaveAndOpenPopup``
- ``TaxesEventHandler::OnTypeChange``
- ``TaxesEventHandler::OnCountryChange``
- ``ListingsEventHandler::OnPreSaveListing``
- ``ListingTypesEventHandler::OnPreSaveListingType``

Входные параметры
-----------------

+-----------------------+------------------------------------------------------------------------+
| название              | описание                                                               |
+=======================+========================================================================+
| .. config-property::  | ``ID`` тех записей, которые необходимо сохранить во временную таблицу. |
|    :name: $items_info |                                                                        |
|    :type: array       |                                                                        |
+-----------------------+------------------------------------------------------------------------+

Вызывает события
----------------

- :doc:`/events/onpresave/on_pre_save_created`

Потенциальное применение
------------------------

Все ситуации, когда нужно сохранить текущую запись во временную таблицу.

.. code:: php

   $event->CallSubEvent('OnPreSaveCreated');

Ограничения
-----------

Нет ограничений.

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnPreSave
