��    s      �              L  �   M  H    �   J
     �
  �       �     �  F     @   V  +   �     �     �  .   �  2   +     ^     n     �     �     �  C   �     �          &  1   E  6   w  "   �  +   �     �  6     �   =     �     �     �     �  !     4  %     Z  =   h  �  �     9     X     a  �   w     n     �  &   �  �   �     Y     m       '  �     �  6   �  	   	          *     @     O     ^     j     {     �  5  �  �   �  n  �  �     �        �  &        +  a   9     �  	   �     �     �     �     �     �  6     �   9     �     �     �        *   /      Z      k      �   $   �      �      �      �   #   �   +   "!     N!  �  e!    $    &     !(     2(     F(     Y(  "   o(     �(  	   �(     �(  a   �(  
   )  %   &)     L)     U)  �   ^)  >   *     U*  �  ]*  *  7,  �  b-  2  1     B2  �  ]2     .5  I   45  \   ~5  Z   �5  K   66  5   �6  R   �6  a   7  o   m7     �7  $   �7     !8  "   >8     a8  E   �8  '   �8  "   �8  :   9  U   L9  X   �9  4   �9  =   0:  !   n:  A   �:  +  �:  
   �;     	<     <     7<  D   G<  >  �<  '   �>  w   �>  �  k?  -   �A     )B  :   @B  �  {B  >   D     YD  :   jD    �D      �E     �E  0   �E  3  F     SH  b   rH     �H  *   �H  *   I     BI  !   bI     �I     �I     �I     �I    �I    �K  �  M  0  �N  �  �O     �Q  R   �Q     R  �   ,R     �R     S  .   #S     RS     _S  /   rS  !   �S  f   �S    +T     >U  "   KU     nU     �U  9   �U     �U  L   �U  )   ?V  $   iV  /   �V     �V  )   �V  /   W  L   8W  0   �W  -  �W  +  �[  �  _     b  $   &b     Kb     kb  7   �b     �b     �b     �b  j   c     c  +   �c     �c     �c    �c  ^   e  
   de   '~LABEL~' will be replaced with the original word. 
 If you just want to add such words for translation, but do not want to mark them separately, then you can only write '~LABEL~' <Tags> that will not be extracted. Usually you don't need to add much here, but if the program constantly extracts something superfluous, then it makes sense to prohibit the extraction of the tag in any way
The first way is to prohibit the extraction of this particular <Tag>. In this case, those tags that completely match the list will not be extracted.
For example <developmentalStageFilter>Baby, Child, Adult</developmentalStageFilter>
Because this line is very similar to normal text, which it would be desirable to extract because there are spaces in it, <tag> should be banned. <Tags> to be extracted for translation, for example, if you want to extract "anima heart" from 
<label>anima heart</label>,
then the list of tags to extract should be "label" <li> class replace A list of <tags> that are in front of a set of consecutive <li> that need to be output
like:<rulePack>
    <rulesStrings>
        <li>RBTStownend->Fieldarmy Base</li>
        <li>RBTStownend->Power Station</li>
        <li>RBTStownend->Powerplant</li>
    </rulesStrings>
</rulePack>

Add tags here only if you are completely sure that Rimworld supports these lists
So, for example, in 1.3 "thoughtStageDescriptions" are not supported, and you have to write each line separately About Add "EN:" before comment text Add <?xml version="1.0" encoding="utf-8"?> at start of Keyed xml files Add <?xml version="1.0" encoding="utf-8"?> at start of xml files Add YOUR image to the original mod preview. Add an image to the preview Add comments to grabbed text Add empty line before each new grabbed defname Add in file comment with FullPath of Original file Add labelFemale Add labelFemalePlural Add labelMale Add labelMalePlural Add labelPlural Add missing tags to choose from in PawnKindDef if they don't exist. Add missing translation Add modDependencies Add stuffAdjective and mark it Add titleFemale if it is not in the original file Add titleShortFemale if it is not in the original file Adding xml-version-encoding string Adding xml-version-encoding string in Keyed Advanced Another Rimworld Mods Folder:
{Path_to_Another_folder} At 1.4 patch TKey system was broken. If the developers fix it, then enable this feature.
 The Tkey system is specifically designed to simplify long tag paths. Author Bottom left Bottom right Center Check at least one letter in text Check if there is at least one letter in the extracted text. This is necessary so as not to extract all sorts of (255, 123, 112).
You may want to remove the flag if the mod adds various symbols without letters that you want to translate like "<--",
I do not know why to translate it at all, but who knows ^_^ Check updates Check updates from GitHub and Download it if find new version Choose the language you are going to translate mods into.
Rimworld has been officially translated into several languages, and in order for your translation of the mod to be automatically added to the game, and not act as a separate new language, use the preset languages from the list
If you want to change the program language, then the language is selected at the top next to the program close button Comment replace \n as new line Comments Copy original patches Delete (Not extract) text for older versions of Rimworld.
By default, the program extracts text for all available versions ( ... 1.0, 1.1, 1.2 ...). You can leave only the newest version, so as not to translate too much (Which I advise you to do) Delete old version folders Description Divide the text into blocks by Defname Empty lines will be added if there are many lines with the same defname in the file. (If the number of different defnames is less than half of all strings.) Enter your language Example About.xml Extraction files rules Files are automatically renamed depending on the folders they fall into. This is necessary to prevent the files from having the same names, which may lead to the fact that the game will not read the translation files.
(Check the box if you don't like it and you want to keep the original titles) Folder Not selected Folder Not selected - Selected path is not Data folder Forbidden Forbidden part of path Forbidden part of tag Forbidden tags Forbidden text Fore spaces General Settings Grabbed lines left spacing Grabbing If you don't trust text extraction from patches - It is many times more complex and the error rate can be high. When this option is enabled - the Program will copy patches that it thinks have text in them, so that you can manually check the extracted text. It will be in a separate folder - “From_patches” If you need to extract all <tags> that have a common part, for example, all <tags> with "Message". Such as:
<NewMessage>Hello</NewMessage>
<OldMessage>Hello</OldMessage>
<Message1>Hello</Message1>
Case-sensitive If you need to prohibit all tags that have a common part of the path: So for
<TraitDef>
   <defName>ReunionCharacter</defName>
   <degreeDatas>
       <li>
           <label>Ally</label>
       </li>
   </degreeDatas>
</TraitDef>
The path to the text "Ally" will be"/TraitDef/ReunionCharacter/degreeDatas/li/label"
And you can prohibit, for example, /degreeDatas/li/ If you need to prohibit extraction of all <tags> that have a common part, for example, all <tags> with "Texture". Such as:
<Texture>Texture1.png</Texture>
<Old_Texture>Texture2.png</Old_Texture>
<MetalTexture>Texture3.png</MetalTexture>
Case-sensitive If you suddenly store mods somewhere else, you can specify this folder here. In this case, the program will work better with mods that depend on other mods (in case the values for translation are inherited from another mod). Image position Left spacing are in before the comment Merge Folders Merge version and Language folders into one Language folder
(If there is only one version folder) New Name No spaces Not rename files One tab Other Part of tag to extraction Pathes to Rimworld folders Place the comment text exactly above the original text Please specify the Data folder of the game, it will help to extract the text better. This is not necessary, but it allows you to find parent-child dependencies. Preview QuestScriptDef Tkey system Rimworld Data:
None Rimworld Data:
{Path_to_Data} Rimworld Mods Folder:
{Path_to_Mod_folder} Russian language Select Another mod folder Select Data folder Select Language of Settings Programm Select MOD folder Select Your image Select path to Rimworld Data Select path to Rimworld Mods Folder Select path to another Rimworld Mods Folder Separating empty lines Some materials can be used to build buildings / make objects, but the authors do not add a special label for this. And in translation it turns out: 'Made of stone'. This is normal for English, but not for some languages.  Therefore, I decided to add a special label to understand how to translate a word as an adjective/ genitive. 
 You can write yourself how to designate such words in the text. To correctly translate such a word, you need to mentally put 'The house is made of' in front of it. 
 '~LABEL~' will be replaced with the original word. If you just want to add such words for translation, but do not want to mark them separately, then you can only write '~LABEL~'. Sometimes TranslationReport wants some <li> to be replaced not with numbers, but with text, depending on "li Class=" for example:
<QuestScriptDef>
  <li Class="QuestNode_Letter">
      <label>Quest expired</label>
  </li>
<QuestScriptDef>

Normally the extracted text would be like this: 
<0.label>Quest expired<0.label> But the game wants him to be like this:
<Letter.label>Quest expired<Letter.label>
And the game takes the "Letter" from the <li> class, so I added the replacement of QuestNode_ with an empty string Sometimes it is necessary to prohibit not the <Tag> but the text. For example, all sorts of true false can sometimes be extracted by the program
<ThingDef>
   <defName>AnimaHeart</defName>
   <useHitPoints_label>true</useHitPoints_label>
</ThingDef>
Since there is a label in the <useHitPoints_label> tag, such a tag may be mistakenly extracted. Therefore, you can either prohibit such a tag, or prohibit the text 'true'. If the text in the Tag completely matches the text added to the prohibited list, it will not be extracted Tags before <li> Tags for extraction Tags to extraction Text Grabber Settings Threshold for adding an empty line Top left Top right Translate mod into: Translate stock->ложe, barrel->ствол, acid fangs->кислотные клыки и т.п. Two spaces tools and death messages into russian x Offset y Offset ~MOD_NAME~ will be replaced with the name of the original mod
~MOD_DESCRIPTION~ will be replaced with the original mod description
~MOD_URL~ will be replaced with the original mod URL ~MOD_NAME~ will be replaced with the name of the original mod. Сommon Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2025-04-05 18:46+0300
PO-Revision-Date: 2023-10-28 22:38+0300
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ru
Language-Team: ru <LL@li.org>
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.17.0
 "~LABEL~" будет заменен исходным словом. 
 Если вы просто хотите добавить такие слова для перевода, но не хотите отмечать их отдельно, то вы можете написать только '~LABEL~' <Тэги>, которые не будут извлечены. Обычно сюда не нужно много добавлять, но если программа постоянно извлекает что-то лишнее, то имеет смысл запретить извлечение тэга каким-либо способом
Первый из способов это запретить извлечения именно этого <Тэга>. В данном случае не будут извлекаться те тэги, которые полностью совпадают со списком
Например <developmentalStageFilter>Baby, Child, Adult</developmentalStageFilter>
Т.к. эта строка очень похожа на нормальный текст, который было бы желательно извлечь т.к. в ней есть пробелы, <Тэг> нужно запретить. <Тэги>, которые будут извлечены для перевода, например, если вы хотите, чтобы было извлечено "anima heart" из 
<label>anima heart</label>,
 то в списке тэгов для извлечения должен быть "label"" Замена в <li Class> Список <тегов>, которые находятся перед набором последовательных <li>, которые необходимо вывести
например:<rulePack>
    <rulesStrings>
        <li>RBTStownend->Fieldarmy Base</li>
        <li>RBTStownend->Power Station</li>
        <li>RBTStownend->Powerplant</li>
    </rulesStrings>
</rulePack>

Добавляйте сюда тэги только если полностью уверены, что Rimworld поддерживает эти списки
Так, например, в 1.3 "thoughtStageDescriptions" не поддерживается, и приходится каждую строчку писать отдельно About Добавлять "EN:" перед текстом комментария Добавлять <?xml version="1.0" encoding="utf-8"?> в начало Keyed файлов Добавлять <?xml version="1.0" encoding="utf-8"?> в начало xml файлов Добавлять СВОЕ изображение в превью в About Добавлять картинку на превью Добавлять комментарии с извлеченным текстом Добавлять пустую строку перед новым извлеченным defname Добавьте в файл комментарий с полным путем к исходному файлу Добавлять labelFemale Добавлять labelFemalePlural Добавлять labelMale Добавлять labelMalePlural Добавлять labelPlural Добавлять отсутствующие теги в PawnKindDef Пропущенные переводы Добавлять modDependencies Добавить stuffAdjective и пометить его Добавлять titleFemale, если его нет в исходном файле Добавьте titleShortFemale, если его нет в исходном файле Добавлять строку xml-version-encoding Добавлять строку xml-version-encoding в Keyed Сложные настройки Другая папка с модами:
{Path_to_Another_folder} В патче 1.4 система TKey была сломана. Если разработчики это исправят, то включите эту функцию.
Система Tkey специально разработана для укорочения длинных путей к тегам" Автор Снизу слева Снизу справа В центре Проверять хотя бы одну букву в тексте Проверять, есть ли в извлеченном тексте хотя бы одна буква. Это необходимо для того, чтобы не извлекать всевозможные (255, 123, 112).
Возможно, вы захотите удалить флаг, если мод добавляет различные символы без букв, которые вы хотите перевести, например, такой как "<--",
Я вообще не знаю, зачем это переводить, но кто знает ^_^ Проверять обновления Проверять обновления с GitHub и скачивать если найдена новая версия Выберите язык, на который вы собираетесь переводить моды   Rimworld официально переведен на несколько языков и для чтобы ваш перевод мода был автоматически добавлен в игру, а не выступал как отдельный новый язык, используйте предустановленные языки из списка.
Если вы хотите изменить язык программы, то язык выбирается вверху рядом с кнопкой закрытия программы" Заменить \n новой строкой Комментарии Скопировать оригинальные патчи Удалять (Не извлекать) текст для старых версий Rimworld.
По умолчанию программа извлекает текст для всех доступных версий ( ... 1.0, 1.1, 1.2 ...). Вы можете оставить только самую новую версию, чтобы не переводить лишнего (Что я вам и советую) Удалить папки со старыми версиями Описание Разделять текст на блоки по Defname Пустые строки будут добавлены в том случае, если в файле много строк с одинаковым defname. (Если количество различных defname меньше половины от всех строк.) Введите свой язык Пример About.xml Правила извлечения файлов Файлы автоматически переименовываются в зависимости от того, в какие папки они попадают. Это необходимо для того, чтобы файлы не имели одинаковых имен, что может привести к тому, что игра не будет читать файлы перевода.
(Установите флажок, если вам это не нравится и вы хотите сохранить оригинальные названия) Папка НЕ выбрана Папка НЕ выбрана - Выбранный путь не содержит папку Data Запрещенное Запрещенные части пути Запрещенные части тега Запрещенные теги Запрещенный текст Четыре пробела Общие настройки Левый отступ Извлечение Если вы не доверяете извлечению текста из патчей - Оно в разы сложнее, и количество ошибок может быть большим. При включении этой опции - Программа скопирует патчи, в которых по ее мнению есть текст, чтобы вы вручную могли проверить извлеченный текст. Он будет в отдельной папке - “From_patches” Если нужно извлечь все <тэги>, имеющие общую часть, например, все <тэги> с "Message". Такие как:
<NewMessage>Hello</NewMessage>
<OldMessage>Hello</OldMessage>
<Message1>Hello</Message1>
Регистр важен Если нужно запретить все тэги, у которых есть общая часть пути: Так для
<TraitDef>
   <defName>ReunionCharacter</defName>
   <degreeDatas>
       <li>
           <label>Ally</label>
       </li>
   </degreeDatas>
</TraitDef>
Путь к тексту "Ally" будет "/TraitDef/ReunionCharacter/degreeDatas/li/label"
А запретить можно, например, /degreeDatas/li/ Если нужно запретить все <тэги>, имеющие общую часть, например, все <тэги> с "Texture". Такие как:
<Texture>Texture1.png</Texture>
<Old_Texture>Texture2.png</Old_Texture>
<MetalTexture>Texture3.png</MetalTexture>
Регистр важен Если вы внезапно храните моды где-то еще, то можете указать эту папку тут. В этом случае программа будет лучше работать с модами, которые зависят от других модов (В случае, если значения для перевода наследуются от другого мода). Позиция картинки Левый интервал находится перед комментарием Объединять папки Объединить папки версий и Language в одну папку Language
(Работает только если существует только одна папка версий) Новое название Без отступа Не переименовывать файлы Один Tab Остальное Часть тега для извлечения Пути к папкам Rimworld Размещать текст комментария точно над исходным текстом Пожалуйста, укажите папку Data игры, это поможет лучше извлечь текст. В этом нет необходимости, но это позволяет найти родительско-дочерние зависимости Превью QuestScriptDef Tkey система Rimworld Data:
None Rimworld Data:
{Path_to_Data} Rimworld Папка с модами:
{Path_to_Mod_folder} Русский язык Выберите дополнительную папку модов Rimworld Выберите папку Rimworld Data Select Language of Settings Programm Выберите папку модов Rimworld Выбрать картинку Выберите папку Rimworld Data Выберите папку модов Rimworld Выберите дополнительную папку модов Rimworld Разделение пустой строкой Из некоторых материалов можно строить здания / делать предметы, но авторы не добавляют специальную метку для этого. И в переводе получается: 'Сделанный из камень'. Для английского языка это нормально, но для некоторых языков нет.  Поэтому я решил добавить специальную метку, чтобы понимать как нужно переводить слово как прилагательное / родительный падеж. 
  Вы можете написать сами как обозначать в тексте такие слова. 
 '~LABEL~' будет заменен на оригинальное слово. Если вы хотите просто добавить такие слова для перевода, но не хотите их отдельно отмечать, то можете написать только '~LABEL~'. Текст до "=" это то, что будет заменяться, текст после - то, на что будет заменятьсяИногда TranslationReport хочет, чтобы некоторые li были заменены не на цифры, а на текст, в зависимости от "li Class=" например:
<QuestScriptDef>
  <li Class="QuestNode_Letter">
      <label>Quest expired</label>
  </li>
<QuestScriptDef>

Обычно извлеченный текст был бы таким: 
<0.label>Quest expired<0.label> Но игра хочет, чтобы он был таким:
<Letter.label>Quest expired<Letter.label>
И "Letter" игра берет из класса <li>, Поэтому я добавил замену QuestNode_ на пустую строку Иногда требуется запретить не <Тег> а текст. Например всякие true false могут иногда извлекаться программой
<ThingDef>
   <defName>AnimaHeart</defName>
   <useHitPoints_label>true</useHitPoints_label>
</ThingDef>
Т.к. в Тэге <useHitPoints_label> есть label, то такой тэг может быть ошибочно извлечен. Поэтому можно как запретить именно такой тэг, так и запретить текст 'true'. Если текст в Тэге будет полностью совпадать с добавленным в список запрещенного текста, то он не будет извлечен Теги перед <li> Тэги для извлечения Извлекаемые теги Text Grabber Настройки Порог добавления пустых строк Вверху слева Вверху справа Перевести мод на Перевести stock->ложe, barrel->ствол, acid fangs->кислотные клыки и т.п. Два пробела tools и death messages на русский Смещение по Х Смещение по У ~MOD_NAME~ будет заменено названим оригинального мода
~MOD_DESCRIPTION~ будет заменено оригинальным описанием мода
~MOD_URL~ будет заменено исходным URL-адресом мода ~MOD_NAME~ будет заменено названием оригинального мода. Общее 