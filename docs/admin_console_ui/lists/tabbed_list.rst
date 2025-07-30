Список с вкладками
==================
`Data Source`_

Список с вкладками - распространённый элемент в K4. Например, в In-Commerce это список заказов (orders).
В In-Auction это списки Listings и журнал запросов к eBay. Данные для нескольких вкладок берутся из одной и
той же основной таблицы. Отличаются лишь некоторые настройки:

- фильтры
- набор отображаемых полей
- кнопки на панели инструментов

Так как вкладки получаются очень похожими, то рекомендуется для них всех использовать по сути один и тот же шаблон.
То есть, на каждую вкладку делается отдельный шаблон, состоящий лишь из одной строки. Например:

.. code:: html

   <inp2:m_include t="in-auction/listings/listing_list" special="failed" grid="Failed"/>

Где ``t`` - общий для всех вкладок шаблон. При этом в параметрах передаются ``special`` и название списка
(ключ в опции :ref:`uc_Grids` в :doc:`Unit Configs </components/unit_configs/config_files>`). Переменный
``special`` позволяет задать для каждого списка свои фильтры в методе ``SetCustomQuery`` соответствующего
event handler-а. Для каждого значения переменной ``grid`` в unit config можно задать свой набор отображаемых
полей. Если на разных вкладках нужны разные кнопки на панели инструментов, то это можно сделать, применив в
общем шаблоне проверку значения ``special``. Например:

.. code:: html

   <inp2:m_if check="m_Param" name="special" equals_to="completed|failed|sold|unsold">
       a_toolbar.AddButton(
           new ToolBarButton(
               'archive',
               '<inp2:m_phrase label="la_ToolTip_Archive" escape="1"/>',
               function() {
                   submit_event('l-ebay.<inp2:m_Param name="special"/>', 'OnArchive');
               }
           )
       );
   </inp2:m_if>


.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81_%D0%B2%D0%BA%D0%BB%D0%B0%D0%B4%D0%BA%D0%B0%D0%BC%D0%B8
