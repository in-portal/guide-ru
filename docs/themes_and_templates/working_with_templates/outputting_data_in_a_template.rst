Вывод данных в шаблоне
======================
`Data Source`_

.. include:: /includes/not_finished.rst

Введение
--------

Данная статья продолжает собой цикл статей, посвящённых синтаксическому анализатору шаблонов (template
parser), использующемуся в платформе. Основной упор делается на описание работы с методами класса
``kDBTagProcessor`` (тэгами):

- ``kApplication::ProcessParsedTag``
- ``kApplication::ParseBlock``

Описан метод ``kDBTagProcessor::prepareTagParams``.

Есть раздел в котором представлена информация, посвященная ограничениям при работе с тэгами.

.. warning::

   .. versionadded:: 4.3.9

      Все примеры предоставлены для самой новой версии парсера, под кодовым названием ``NParser``.

Метод "kApplication::ProcessParsedTag"
--------------------------------------

Данный метод нужен для того, чтобы вызвать метод другого обработчика тэгов (tag processor).

Параметры вызова
^^^^^^^^^^^^^^^^

+----------------------+-----------------------------------------------------+
| параметр             | описание                                            |
+======================+=====================================================+
| .. config-property:: | :ref:`префикс <uc_Prefix>` тэга, например ``test``. |
|    :name: prefix     |                                                     |
|    :type: string     |                                                     |
+----------------------+-----------------------------------------------------+
| .. config-property:: | тэг, т.е. название метода другого обработчика тэгов |
|    :name: tag        | (tag processor).                                    |
|    :type: string     |                                                     |
+----------------------+-----------------------------------------------------+
| .. config-property:: | массив параметров, которые можно передать.          |
|    :name: params     |                                                     |
|    :type: string     |                                                     |
+----------------------+-----------------------------------------------------+

Пример
^^^^^^

Вызывается метод ``t`` префикса ``m`` c типичными для такого метода параметрами.

.. code:: php

   function LoginLink($params)
   {
       $params['t'] = 'login';
       $params['pass'] = 'm';
       $params['m_cat_id'] = 0;
       return $this->Application->ProcessParsedTag('m', 't', $params);
   }

Применение ``kApplication::ProcessParsedTag`` метода позволяет вызывать тэги, других (не
связанных с друг другом) обработчиков тэгов (tag processors), что в повседневной работе
дает еще больше возможности для повторного применения уже написанного кода.

Метод "kApplication::ParseBlock"
--------------------------------

Метод ``kApplication::ParseBlock`` - это стандартный способ вывести в шаблон результат работы
любого, доступного в текущем шаблон, блока.

Параметры вызова
^^^^^^^^^^^^^^^^

+-----------------------+----------------------------------------------------------------------+
| параметр              | описание                                                             |
+=======================+======================================================================+
| .. config-property::  | Массив содержит параметры, которые передаются в блок. Обязательный   |
|    :name: params      | параметр - это ``name``, т.е. имя блока или шаблона. В этом массиве  |
|    :type: array       | можно задавать сколько угодно дополнительных параметров.             |
+-----------------------+----------------------------------------------------------------------+
| .. config-property::  | По умолчанию равен 0, если установлено отличное от нуля значение,    |
|    :name: pass_params | то в вызываемый блок будут переданы параметры доступны на самом      |
|    :type: int         | шаблоне.                                                             |
+-----------------------+----------------------------------------------------------------------+
| .. config-property::  | По умолчанию равен ``false``, если установлено значение ``true``,    |
|    :name: as_template | то метод парсит не блок, а шаблон с таким именем. Если нет такого    |
|    :type: int         | в папке с темой проекта, то будет выдано сообщение об ошибке в       |
|                       | :doc:`отладчике </application_debugging/debugger>`.                  |
+-----------------------+----------------------------------------------------------------------+

Пример
^^^^^^

Использование ``kApplication::ParseBlock`` метода в ``<inp2:custom-sections_PrintNumbers .../>``
тэге объявленном в ``CustomTagProcessor`` классе от ``custom-sections`` unit:

.. code:: php

   function PrintNumbers($params)
   {
       $o = '';

       $block_params = $this->prepareTagParams($params);
       $block_params['name'] = $this->SelectParam($params, 'render_as,block');

       for ($i = 1; $i <= 5 ; $i++ ) {
           $block_params['number'] = $i;
           $o.= $this->Application->ParseBlock($block_params);
       }
       return $o;
   }

Использование ``<inp2:custom-sections_PrintNumbers .../>`` на шаблоне:

.. code:: html

   // Описание блока
   <inp2:m_DefineElement name="menu_block">
   <inp2:m_Param name="number"/><br />
   </inp2:m_DefineElement>

   // Вызов custom-sections_PrintNumbers тэга
   <inp2:custom-sections_PrintNumbers render_as="menu_block" />

   // Результат работы custom-sections_PrintNumbers тэга
   1
   2
   3
   4
   5

Метод "kDBTagProcessor::prepareTagParams"
-----------------------------------------

Данный метод предназначен для упрощения задания параметров префикса и ``special`` в других тегах,
главным образом для тех, которые для вывода данных используют метод ``kApplication::ParseBlock``.

Метод ``kDBTagProcessor::prepareTagParams`` принимает в качестве параметра ассоциативный массив
``$params`` и добавляет в него значения префикса и ``special``.

Результатом работы метода является ассоциативный массив вида:

.. code:: php

   Array(
       // другие параметры
       'Prefix' => 'my-test-prefix'
       'Special' => 'my-test-special'
       'PrefixSpecial' => 'my-test-prefix.my-test-special'
   );

Пример
^^^^^^

Пример тэга ``PrintList``, который выводит список товаров заказа для префикса ``my-test-prefix``.

Хорошо видно как массив ``$params`` передается в метод ``kDBTagProcessor::prepareTagParams`` и
результат работы записываются в другой массив ``$block_params``, который в свою очередь уже
передается в метод ``kApplication::ParseBlock``.

.. code:: php

   function PrintList($params)
   {
       $list =& $this->GetList($params);
       $list->Query();
       $o = '';
       $list->GoFirst();

       $block_params = $this->prepareTagParams($params);
       $block_params['name'] = $this->SelectParam($params, 'render_as,block');

       while (!$list->EOL()) {
           $o.= $this->Application->ParseBlock($block_params, 1);
           $list->GoNext();
       }
       return $o;
   }

Использование в шаблоне:

.. code:: html

   // декларация блока "my_test_row"
   <inp2:m_DefineElement name="my_test_row">
   <tr>
       <td><inp2:Field field="ProductName"/></td>
       <td><inp2:Field field="Quantity"/></td>
       <td><inp2:Field field="Price"/></td>
   </tr>
   </inp2:m_DefineElement>

   // вызов "my_test_row" блока
   <inp2:mytestprefix_PrintList block="my_test_row"/>

Можно иногда для тэга ``Field`` встретить такой вызов ``<inp2:{$PrefixSpecial}_Field field="ProductName"/>``.

Это означает, что ``PrefixSpecial`` жестко передается для тэга ``Field``. Сейчас такую конструкцию
применять не нужно, т.к. есть метод ``kDBTagProcessor::prepareTagParams`` которые устанавливает эти
параметры.

Ограничения на объявление блоков (чего точно не будет работать)
---------------------------------------------------------------

При объявление блока нужно следовать правилам.

- Нельзя объявить 2 блока с одинаковым именем и ждать, что будет использован первый объявленный.
  В таком случае будет использоваться второй блок.

.. code:: html

   // первое объявление блока
   <inp2:DefineElement name="my_test_block">
   Hello World !
   </inp2:DefineElement>

   // второе объявление блока
   <inp2:DefineElement name="my_test_block">
   Hello Everyone !
   </inp2:DefineElement>

При вызове на шаблоне блока ``my_test_block`` будет выведено

.. code:: html

   Hello Everyone !

- Если объявить блок внутри тэгa ``m_if`` или другого парного тэга, то блок будет объявлен
  только когда сработает IF.

Пример тэга ``m_if`` для показа ошибки при логине.

.. code:: html

   <inp2:m_if check="u_HasError" field="ValidateLogin">

       <inp2:m_DefineElement name="error_message">
       Special error message
       </inp2:m_DefineElement>

       <inp2:u_Error field="ValidateLogin" />

   </inp2:m_if>

   // Вызов блока
   <inp2:m_RenderElement name="error_message" />

При попадании на такую страницу, будет выведена ошибка :doc:`отладчика </application_debugging/debugger>`.

.. code::

   Fatal Error: Rendering of undefined element error_message

- При определение блока нужно применять только конструкцию ``DefineElement``. Раньше можно
  было также применять ``block .. blockend``.

.. code:: html

   // правильный вариант
   <inp2:m_DefineElement name="valid_block">
   Block body
   </inp2:m_DefineElement>

   // устаревший способ
   <inp2:m_block name="invalid_block">
   Block body
   <inp2:m_blockend/>

При попадании на такую страницу, будет выведена ошибка :doc:`отладчика </application_debugging/debugger>`.

.. code::

   Fatal Error: Tag without a handler: m_block  - probably missing <empty /> tag closing

- Нужно быть внимательнее с знаком ``/`` в написание блока ``DefineElement``. Если забыть
  закрывающий ``/`` как в примере.

.. code:: html

   <inp2:m_DefineElement name="error_message">
       Special error message
   <inp2:m_DefineElement>

При попадании на такую страницу, будет выведена ошибка :doc:`отладчика </application_debugging/debugger>`.

.. code::

   Fatal Error: Tag m_DefineElement  called  without required name  attribute in w:\newsletter\themes\theme_newsletter\index.tpl on line 6

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:%D0%92%D1%8B%D0%B2%D0%BE%D0%B4_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85_%D0%B2_%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B5
