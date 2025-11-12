OnListBuild
===========
`Data Source`_

.. include:: /includes/not_finished.rst

При создании объекта класса ``kDBList`` требуется производить сопутствующие действия - такие как подготовка
SQL-запроса для загрузки данных, установление связи с главным объектом если таковой имеется, создание и
инициализация переменных окружения, инициализация свойств объекта. Для логического выделения этих операций в
общем потоке предназначено особое событие - ``OnListBuild``.

Это событие задаётся в :doc:`Unit Configs </components/unit_configs/config_files>`, под ключом ``build_event``
для ``ListClass``.

.. code:: php

   'ListClass' => Array ('class' => 'kDBList', 'file' => '', 'build_event' => 'OnListBuild'),

Это событие вызывается в классе ``kFactory``, после того как создан новый экземпляр объекта. Если в создании
нового экземпляра нет необходимости, то методы ``kFactory`` возвращают ссылку на ранее созданный экземпляр,
и событие ``OnItemBuild`` не происходит.

Вызывается из шаблона
---------------------

Не вызывается из шаблонов.

Вызывается из событий
---------------------

Не вызывается из событий.

Входные параметры
-----------------

В событие могут быть переданы любые параметры. Если объект создаётся при обработке тэга, то в событие передаются
все параметры тэга. Если объект создаётся методами типа ``getObject``, ``recallObject`` и.т.п., то в этих методах
один из параметров является массивом, и ключи этого массива в итоге оказываются параметрами для события
``OnListBuild``. Событие ``OnListBuild`` не использует переданные ему параметры, а лишь передаёт их транзитом
вызываемым методам в составе параметра ``&$event``.

Вызывает события
----------------

Не вызывает событий

Потенциальное применение
------------------------

В простых, стандартных случаях настройка и конфигурирование объекта делается в
:doc:`Unit Configs </components/unit_configs/config_files>`. В прочих ситуациях настройку можно завершить,
дописав код к событию ``OnListBuild``. Например, известно, что опции для фильтров в списке можно задавать
SQL-запросом, и это можно делать в Unit Configs. Но если ситуация немного сложнее, и для получения списка
опций нужен не один, а два последовательных запроса, то в Unit Configs это не получится, а в событии
``OnListBuild`` - без проблем:

.. code:: php

   parent::OnListBuild($event);
   $object =& $event->getObject();
   /* @var $object kDBList */

   $some_options = $object->GetFieldOptions('SomeField');
   $some_options['options'] = $this->getComplicatedFieldOptions();
   $object->SetFieldOptions('SomeField', $some_options);

В примере подразумевается что метод ``getComplicatedFieldOptions`` возвращает опции, выбираемые по сложному алгоритму.

Ограничения
-----------

Особых ограничений нет.

Использует вспомогательные методы класса
----------------------------------------

- ``kDBEventHandler::dbBuild``
- ``kDBEventHandler::ListPrepareQuery``
- ``kDBEventHandler::getMainSpecial``
- ``kDBEventHandler::AddFilters``
- :doc:`/events/lists/set_custom_query`
- ``kDBEventHandler::SetPagination``
- ``kDBEventHandler::SetSorting``

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnListBuild
