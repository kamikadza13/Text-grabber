��    p      �                �     H  �  �   
     �
  �  �
     �  	   �     �  +   �     +     G  )   d  2   �     �     �     �     �     	  C        ]     q  1   �  6   �     �  6     �   B     �     �     �       !     4  *     _  =   m  �  �  �  E     �       �             &  &   2  �   Y     �     �          '     9  C   P     �  '  �  	   �     �     �               $     5     P  �   Y  n  -  �   �  �   �     y  &   �     �  a   �       U   (     ~  	   �     �     �     �     �     �     �     �  6        N     V     q  *   �     �     �  $   �                 0      A   #   ^   +   �   �  �     T#    Z%     j'     r'     �'     �'     �'     �'  E   �'  "   (     8(  	   A(  
   K(     V(     ](     f(  �   o(  >   ')  �  f)  �   �*  H  �+  �   �-     �.  �  �.     �0  	   �0     �0  +   �0     1      1  )   =1  2   g1     �1     �1     �1     �1     �1  C   �1     62     J2  1   i2  6   �2     �2  6   �2  �   3     �3     �3     �3     �3  !   �3  4  4     85  =   F5  �  �5  �  7     �8     �8  �   �8     �9     �9  &   �9  �   %:     �:     �:     �:     �:     ;  C   ;     `;  '  s;  	   �<     �<     �<     �<     �<     �<     =     =  �   %=  n  �=  �   h?  �   d@     EA  &   TA     {A  a   �A     �A  U   �A     JB  	   fB     pB     uB     �B     �B     �B     �B     �B  6   �B     C     "C     =C  *   [C     �C     �C  $   �C     �C     �C     �C     D  #   *D  +   ND  �  zD  _   G    �I     �K     �K     �K     �K     �K     �K  E   �K  "   ;L     ^L  	   gL  
   qL     |L     �L     �L  �   �L  >   MM   '~LABEL~' will be replaced with the original word. 
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
So, for example, in 1.3 "thoughtStageDescriptions" are not supported, and you have to write each line separately A new value has been found! About.xml Add "EN:" before comment text Add YOUR image to the original mod preview. Add an image to the preview Add comments to grabbed text Add empty line before new grabbed defname Add in file comment with FullPath of Original file Add labelFemale Add labelFemalePlural Add labelMale Add labelMalePlural Add labelPlural Add missing tags to choose from in PawnKindDef if they don't exist. Add modDependencies Add stuffAdjective and mark it Add titleFemale if it is not in the original file Add titleShortFemale if it is not in the original file Advanced settings Another Rimworld Mods Folder:
{Path_to_Another_folder} At 1.4 patch TKey system was broken. If the developers fix it, then enable this feature.
 The Tkey system is specifically designed to simplify long tag paths. Author Bottom left Bottom right Center Check at least one letter in text Check if there is at least one letter in the extracted text. This is necessary so as not to extract all sorts of (255, 123, 112).
You may want to remove the flag if the mod adds various symbols without letters that you want to translate like "<--",
I do not know why to translate it at all, but who knows ^_^ Check updates Check updates from GitHub and Download it if find new version Choose the language you are going to translate mods into.
   Rimworld has been officially translated into several languages, and in order for your translation of the mod to be automatically added to the game, and not act as a separate new language, use the preset languages from the list.
  If you want to change the program language, then the language is selected at the top next to the program close button. Choose the language you are going to translate mods into.
   Rimworld официально переведен на несколько языков и для чтобы ваш перевод мода был автоматически добавлен в игру, а не выступал как отдельный новый язык, используйте предустановленные языки из списка. Comment replace \n as new line Comments Delete (Not extract) text for older versions of Rimworld.
By default, the program extracts text for all available versions ( ... 1.0, 1.1, 1.2 ...). You can leave only the newest version, so as not to translate too much (Which I advise you to do) Delete old version folders Description Divide the text into blocks by Defname Empty lines will be added if there are many lines with the same defname in the file. (If the number of different defnames is less than half of all strings.) En Enter your language Error reading {file_name} Example About.xml Extraction files rules FOUNDED NEW VALUE - {option_name}
Please Check tab {option_section} FOUNDED NEW VALUE! Files are automatically renamed depending on the folders they fall into. This is necessary to prevent the files from having the same names, which may lead to the fact that the game will not read the translation files.
(Check the box if you don't like it and you want to keep the original titles) Forbidden Forbidden part of path Forbidden part of tag Forbidden tags Forbidden text General Settings Grabbed lines left spacing Grabbing If you need to extract all <tags> that have a common part, for example, all <tags> with "Message". Such as:
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
(If there is only one version folder) New Name New values have been found in sections - {option_section}
Please Check {option_names} New values have been found! No spaces None Not rename files One tab Other Part of tag to extraction Pathes to Rimworld folders PawnKindDef Plural labels Place the comment text exactly above the original text Preview QuestScriptDef Tkey system Rimworld Data:
{Path_to_Data} Rimworld Mods Folder:
{Path_to_Mod_folder} Select Another mod folder Select Data folder Select Language of Settings Programm Select MOD folder Select Your image Select language: Select path to Rimworld Data Select path to Rimworld Mods Folder Select path to another Rimworld Mods Folder Some materials can be used to build buildings / make objects, but the authors do not add a special label for this. And in translation it turns out: 'Made of stone'. This is normal for English, but not for some languages.  Therefore, I decided to add a special label to understand how to translate a word as an adjective/ genitive. 
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
Since there is a label in the <useHitPoints_label> tag, such a tag may be mistakenly extracted. Therefore, you can either prohibit such a tag, or prohibit the text 'true'. If the text in the Tag completely matches the text added to the prohibited list, it will not be extracted Spacing StuffAdjective Tags before <li> Tags for extraction Tags to extraction Text Grabber Settings The settings have been moved to AppData\Roaming\Text_grabber\Settings Threshold for adding an empty line Top left Top right Two spaces Update x Offset y Offset ~MOD_NAME~ will be replaced with the name of the original mod
~MOD_DESCRIPTION~ will be replaced with the original mod description
~MOD_URL~ will be replaced with the original mod URL ~MOD_NAME~ will be replaced with the name of the original mod. Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2023-12-19 17:22+0300
PO-Revision-Date: 2023-10-28 22:38+0300
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: en
Language-Team: en <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.13.0
 '~LABEL~' will be replaced with the original word. 
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
So, for example, in 1.3 "thoughtStageDescriptions" are not supported, and you have to write each line separately A new value has been found! About.xml Add "EN:" before comment text Add YOUR image to the original mod preview. Add an image to the preview Add comments to grabbed text Add empty line before new grabbed defname Add in file comment with FullPath of Original file Add labelFemale Add labelFemalePlural Add labelMale Add labelMalePlural Add labelPlural Add missing tags to choose from in PawnKindDef if they don't exist. Add modDependencies Add stuffAdjective and mark it Add titleFemale if it is not in the original file Add titleShortFemale if it is not in the original file Advanced settings Another Rimworld Mods Folder:
{Path_to_Another_folder} At 1.4 patch TKey system was broken. If the developers fix it, then enable this feature.
 The Tkey system is specifically designed to simplify long tag paths. Author Bottom left Bottom right Center Check at least one letter in text Check if there is at least one letter in the extracted text. This is necessary so as not to extract all sorts of (255, 123, 112).
You may want to remove the flag if the mod adds various symbols without letters that you want to translate like "<--",
I do not know why to translate it at all, but who knows ^_^ Check updates Check updates from GitHub and Download it if find new version Choose the language you are going to translate mods into.
   Rimworld has been officially translated into several languages, and in order for your translation of the mod to be automatically added to the game, and not act as a separate new language, use the preset languages from the list.
  If you want to change the program language, then the language is selected at the top next to the program close button. Choose the language you are going to translate mods into.
   Rimworld has been officially translated into several languages, and in order for your translation of the mod to be automatically added to the game, and not act as a separate new language, use the preset languages from the list.
  If you want to change the program language, then the language is selected at the top next to the program close button. Comment replace \n as new line Comments Delete (Not extract) text for older versions of Rimworld.
By default, the program extracts text for all available versions ( ... 1.0, 1.1, 1.2 ...). You can leave only the newest version, so as not to translate too much (Which I advise you to do) Delete old version folders Description Divide the text into blocks by Defname Empty lines will be added if there are many lines with the same defname in the file. (If the number of different defnames is less than half of all strings.) En Enter your language Error reading {file_name} Example About.xml Extraction files rules FOUNDED NEW VALUE - {option_name}
Please Check tab {option_section} FOUNDED NEW VALUE! Files are automatically renamed depending on the folders they fall into. This is necessary to prevent the files from having the same names, which may lead to the fact that the game will not read the translation files.
(Check the box if you don't like it and you want to keep the original titles) Forbidden Forbidden part of path Forbidden part of tag Forbidden tags Forbidden text General Settings Grabbed lines left spacing Grabbing If you need to extract all <tags> that have a common part, for example, all <tags> with "Message". Such as:
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
(If there is only one version folder) New Name New values have been found in sections - {option_section}
Please Check {option_names} New values have been found! No spaces None Not rename files One tab Other Part of tag to extraction Pathes to Rimworld folders PawnKindDef Plural labels Place the comment text exactly above the original text Preview QuestScriptDef Tkey system Rimworld Data:
{Path_to_Data} Rimworld Mods Folder:
{Path_to_Mod_folder} Select Another mod folder Select Data folder Select Language of Settings Programm Select MOD folder Select Your image Select language: Select path to Rimworld Data Select path to Rimworld Mods Folder Select path to another Rimworld Mods Folder Some materials can be used to build buildings / make objects, but the authors do not add a special label for this. And in translation it turns out: 'Made of stone'. This is normal for English, but not for some languages.  Therefore, I decided to add a special label to understand how to translate a word as an adjective/ genitive. 
 You can write yourself how to designate such words in the text. To correctly translate such a word, you need to mentally put 'The house is made of' in front of it. 
 '~LABEL~' will be replaced with the original word. If you just want to add such words for translation, but do not want to mark them separately, then you can only write '~LABEL~'. The text before "=" is what will be replaced, the text after is what will be replaced withSometimes TranslationReport wants some <li> to be replaced not with numbers, but with text, depending on "li Class=" for example:
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
Since there is a label in the <useHitPoints_label> tag, such a tag may be mistakenly extracted. Therefore, you can either prohibit such a tag, or prohibit the text 'true'. If the text in the Tag completely matches the text added to the prohibited list, it will not be extracted Spacing StuffAdjective Tags before <li> Tags for extraction Tags to extraction Text Grabber Settings The settings have been moved to AppData\Roaming\Text_grabber\Settings Threshold for adding an empty line Top left Top right Two spaces Update x Offset y Offset ~MOD_NAME~ will be replaced with the name of the original mod
~MOD_DESCRIPTION~ will be replaced with the original mod description
~MOD_URL~ will be replaced with the original mod URL ~MOD_NAME~ will be replaced with the name of the original mod. 