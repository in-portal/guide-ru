Regular Events
==============
`Data Source`_
`Eng Data Source`_

В K4 существует механизм, позволяющий выполнять требуемые :doc:`события </events>` в системе на
регулярной основе. Т.е. вызывать указанное событие раз в ``N`` секунд. Есть 2 способа вызова
(когда их вызывает система) данных событий:

- из скрипта ``tools/cron.php``;
- до или после показывания содержания страницы пользователю.

У каждого из этих способов есть свои плюсы и минусы, зная которые можно вернее принять решение
о том, какой из них использовать. Переключаться можно способом вызова регулярных событий можно
используя опцию :ref:`cfg_UseCronForRegularEvent` в конфигурации сайта.

С использованием cron
---------------------

Неоспоримым плюсом при использовании ``cron`` является то, что пользователи, заходящие на сайт не
будут ждать выполнения долгих регулярных событий. Этот способ хорошо подходит для случаев, когда
результат работы регулярного события не сразу можно увидеть на сайте. Хорошим примером этому может
служить регулярное событие, которое обновляет рейтинг пользователей. Пользователей на сайте может
быть много, а пересчёт их рейтинга при заходе других пользователей на сайт может занять значительное
время. В результате увеличится время, требуемое для показывания странички пользователю и он просто
может уйти с сайта не дождавшись результата. Если для обработки регулярных событий использовать cron,
то этой проблемы не будет.

Длй настройки cron на сайте требуется добавить следующую команду в файл crontab (используя команду
``crontab -e``) текущего пользователя:

.. code:: bash

   wget http://server_address/tools/cron.php -O /dev/null > /dev/null 2>&1

- ``server_address`` - это путь, который используется для захода на сайт из браузера (напр.
  ``alex.prod.intechnic.lv/test_project``).

В этом случае регулярные события не будут выполняться при заходе на сайт, а будут выполняться при
вызове файла ``tools/cron.php`` (брать из In-Portal).

Без использования cron
----------------------

Если cron не используется или его не представляется возможным включить на сайте, то можно воспользоваться
способом вызова регулярных событий по умолчанию. Данных способ сильно уступает ранее описанному, но не
требует никакой дополнительной настройки сайта и доступен каждому. В более поздних версия K4 можно
ставить :doc:`after hook </components/unit_configs/hooks>` на события:

.. versionadded:: 4.0.0

   - ``adm:OnStartup`` - для выполнения событий до показывания страницы;

.. versionadded:: 4.2.1

   - ``adm:OnBeforeShutdown`` - для выполнения событий после показывания страницы;

Если требуется, чтобы событие **выполнялось всегда** (в случае с регулярными событиями оно выполняется раз
в ``N`` секунд), то рекомендуется использовать этот подход.

Пример
------

Для того, чтобы добавить новое регулярное событие его надо сначала написать, а потом в его |unit_config_link|
в опции :ref:`uc_RegularEvents` добавить новый ключ:

.. code:: php

    'RegularEvents' => Array (
        'membership_expiration' => Array (
            'EventName' => 'OnCheckExpiredMembership', 'RunInterval' => 1800, 'Type' => reAFTER
        ),
    ),

Название ключа должно быть уникальным среди всех зарегистрированных в системе регулярных событий.

+--------------------------------+-----------------------------------------------------------------------------+
| название опции                 | описание опции                                                              |
+================================+=============================================================================+
| .. config-property::           | Название события в текущем |unit_config_link|.                              |
|    :name: EventName            |                                                                             |
|    :type: string               |                                                                             |
|    :ref_prefix: regular_event_ |                                                                             |
+--------------------------------+-----------------------------------------------------------------------------+
| .. config-property::           | Интервал, с которым данное событие должно вызываться (в секундах).          |
|    :name: RunInterval          |                                                                             |
|    :type: int                  |                                                                             |
|    :ref_prefix: regular_event_ |                                                                             |
+--------------------------------+-----------------------------------------------------------------------------+
| .. config-property::           | Определяет когда вызывать данное событие относительно показывания страницы: |
|    :name: Type                 |                                                                             |
|    :type: int, const           | - ``reBEFORE`` - до показывания страницы;                                   |
|    :ref_prefix: regular_event_ | - ``reAFTER`` - после показывания страницы.                                 |
+--------------------------------+-----------------------------------------------------------------------------+

.. _Data Source: http://guide.in-portal.org/rus/index.php/K4:Regular_Events
.. _Eng Data Source: http://guide.in-portal.org/eng/index.php/Regular_Events

.. |unit_config_link| replace:: :doc:`unit config </components/unit_configs/config_files>`
