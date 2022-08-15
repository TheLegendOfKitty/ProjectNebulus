from __future__ import annotations

import json

import schoolopy
from flask import session
from mongoengine import Q

from app.static.python.utils.security import valid_password
from ..classes import *

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

dictionary = {
  "Nebulus": {
    "us": "Nebulus",
    "uk": "Nebulus",
    "au": "Nebulus",
    "es": "N\u00e9bulus",
    "mx": "N\u00e9bulus",
    "cr": "N\u00e9bulus",
    "cu": "N\u00e9bulus",
    "co": "N\u00e9bulus",
    "ar": "N\u00e9bulus",
    "it": "N\u00e8bulo",
    "cn": "\u8010\u535a\u4e50\u601d",
    "tw": "\u8010\u535a\u6a02\u601d",
    "hk": "\u8010\u535a\u6a02\u601d",
    "mo": "\u8010\u535a\u6a02\u601d",
    "jp": "\u30cd\u30d3\u30e5\u30e9\u30b9",
    "kr": "\ub124\ubdf8\ub7ec\uc2a4"
  },
  "Learning": {
    "us": "Learning",
    "uk": "United Kingdom",
    "au": "Australia",
    "es": "Espa\u00f1a",
    "mx": "M\u00e9xico",
    "cr": "Costa Rica",
    "cu": "Cuba",
    "co": "Colombia",
    "ar": "Argentina",
    "it": "Italia",
    "cn": "\u4e2d\u56fd\u5927\u9646",
    "tw": "\u53f0\u7063",
    "hk": "\u9999\u6e2f",
    "mo": "\u6fb3\u9580",
    "jp": "\u65e5\u672c",
    "kr": "\ub300\ud55c\ubbfc\uad6d \uc0ac\ub78c"
  },
  "A Learning, All In One Experience": {
    "us": "A Learning, All In One Experience",
    "uk": "A Learning, All In One Experience",
    "au": "A Learning, All In One Experience",
    "es": "Una Experiencia de Aprendizaje todo en Uno",
    "mx": "Una Experiencia de Aprendizaje todo en Uno",
    "cr": "Una Experiencia de Aprendizaje todo en Uno",
    "cu": "Una Experiencia de Aprendizaje todo en Uno",
    "co": "Una Experiencia de Aprendizaje todo en Uno",
    "ar": "Una Experiencia de Aprendizaje todo en Uno",
    "cn": "\u4e00\u4e2a\u6709\u8da3\uff0c\u5168\u9762\u7684\u5b66\u4e60\u5e73\u53f0",
    "tw": "\u4e00\u4e2a\u6709\u8da3\uff0c\u5168\u9762\u7684\u5b66\u4e60\u5e73\u53f0",
    "hk": "\u4e00\u4e2a\u6709\u8da3\uff0c\u5168\u9762\u7684\u5b66\u4e60\u5e73\u53f0",
    "mo": "\u4e00\u4e2a\u6709\u8da3\uff0c\u5168\u9762\u7684\u5b66\u4e60\u5e73\u53f0",
    "kr": "\ud558\ub098\uc758 \uacbd\ud5d8\uc5d0\uc11c \ubc30\uc6b0\ub294 \ud559\uc2b5"
  },
  "Nebulus. Education. Redefined.": {
    "us": "Nebulus. Education. Redefined",
    "uk": "Nebulus. Education. Redefined",
    "au": "Nebulus. Education. Redefined",
    "es": "N\u00e9bulus. Educaci\u00f3n. Redefinida.",
    "mx": "N\u00e9bulus. Educaci\u00f3n. Redefinida.",
    "cr": "N\u00e9bulus. Educaci\u00f3n. Redefinida.",
    "cu": "N\u00e9bulus. Educaci\u00f3n. Redefinida.",
    "co": "N\u00e9bulus. Educaci\u00f3n. Redefinida.",
    "ar": "N\u00e9bulus. Educaci\u00f3n. Redefinida.",
    "it": "Nebulo. Istruzione. Ridefinito.",
    "cn": "\u8010\u535a\u4e50\u601d\uff1a\u521b\u65b0\u7684\u6559\u80b2\u65b9\u5f0f\u3002",
    "tw": "\u8010\u535a\u6a02\u601d\uff1a\u5275\u65b0\u7684\u6559\u80b2\u65b9\u5f0f\u3002",
    "hk": "\u8010\u535a\u6a02\u601d\uff1a\u5275\u65b0\u7684\u6559\u80b2\u65b9\u5f0f\u3002",
    "mo": "\u8010\u535a\u6a02\u601d\uff1a\u5275\u65b0\u7684\u6559\u80b2\u65b9\u5f0f\u3002",
    "jp": "\u30cd\u30d3\u30e5\u30e9\u30b9\u3002\u65b0\u3057\u3044\u6559\u80b2\u306e\u59cb\u307e\u308a\u3002",
    "kr": "\ub124\ubdf8\ub7ec\uc2a4.  \uad50\uc721.  \uc7ac\uc815\uc758."
  },
  "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.": {
    "us": "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.d",
    "uk": "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.",
    "au": "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.",
    "es": "N\u00e9bulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en N\u00e9bulus para acceder a ellas f\u00e1cilmente. Tambi\u00e9n te puedes organizar con N\u00e9bulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. \u00a1Todo est\u00e1 organizado para ti de manera f\u00e1cil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. \u00a1Por eso, hemos a\u00f1adido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisi\u00f3n de ex\u00e1menes y mucho m\u00e1s. Tambi\u00e9n contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. \u00a1Tenemos integraciones que te permiten tener una calculadora, una calculadora gr\u00e1fica, un diccionario, un comprobador de plagio, un mapamundi, una tabla peri\u00f3dica, un editor de c\u00f3digo y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho m\u00e1s! Estamos a\u00f1adiendo muchos m\u00e1s aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
    "mx": "N\u00e9bulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en N\u00e9bulus para acceder a ellas f\u00e1cilmente. Tambi\u00e9n te puedes organizar con N\u00e9bulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. \u00a1Todo est\u00e1 organizado para ti de manera f\u00e1cil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. \u00a1Por eso, hemos a\u00f1adido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisi\u00f3n de ex\u00e1menes y mucho m\u00e1s. Tambi\u00e9n contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. \u00a1Tenemos integraciones que te permiten tener una calculadora, una calculadora gr\u00e1fica, un diccionario, un comprobador de plagio, un mapamundi, una tabla peri\u00f3dica, un editor de c\u00f3digo y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho m\u00e1s! Estamos a\u00f1adiendo muchos m\u00e1s aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
    "cr": "N\u00e9bulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en N\u00e9bulus para acceder a ellas f\u00e1cilmente. Tambi\u00e9n te puedes organizar con N\u00e9bulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. \u00a1Todo est\u00e1 organizado para ti de manera f\u00e1cil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. \u00a1Por eso, hemos a\u00f1adido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisi\u00f3n de ex\u00e1menes y mucho m\u00e1s. Tambi\u00e9n contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. \u00a1Tenemos integraciones que te permiten tener una calculadora, una calculadora gr\u00e1fica, un diccionario, un comprobador de plagio, un mapamundi, una tabla peri\u00f3dica, un editor de c\u00f3digo y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho m\u00e1s! Estamos a\u00f1adiendo muchos m\u00e1s aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
    "cu": "N\u00e9bulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en N\u00e9bulus para acceder a ellas f\u00e1cilmente. Tambi\u00e9n te puedes organizar con N\u00e9bulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. \u00a1Todo est\u00e1 organizado para ti de manera f\u00e1cil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. \u00a1Por eso, hemos a\u00f1adido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisi\u00f3n de ex\u00e1menes y mucho m\u00e1s. Tambi\u00e9n contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. \u00a1Tenemos integraciones que te permiten tener una calculadora, una calculadora gr\u00e1fica, un diccionario, un comprobador de plagio, un mapamundi, una tabla peri\u00f3dica, un editor de c\u00f3digo y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho m\u00e1s! Estamos a\u00f1adiendo muchos m\u00e1s aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
    "co": "N\u00e9bulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en N\u00e9bulus para acceder a ellas f\u00e1cilmente. Tambi\u00e9n te puedes organizar con N\u00e9bulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. \u00a1Todo est\u00e1 organizado para ti de manera f\u00e1cil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. \u00a1Por eso, hemos a\u00f1adido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisi\u00f3n de ex\u00e1menes y mucho m\u00e1s. Tambi\u00e9n contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. \u00a1Tenemos integraciones que te permiten tener una calculadora, una calculadora gr\u00e1fica, un diccionario, un comprobador de plagio, un mapamundi, una tabla peri\u00f3dica, un editor de c\u00f3digo y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho m\u00e1s! Estamos a\u00f1adiendo muchos m\u00e1s aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
    "ar": "N\u00e9bulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en N\u00e9bulus para acceder a ellas f\u00e1cilmente. Tambi\u00e9n te puedes organizar con N\u00e9bulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. \u00a1Todo est\u00e1 organizado para ti de manera f\u00e1cil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. \u00a1Por eso, hemos a\u00f1adido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisi\u00f3n de ex\u00e1menes y mucho m\u00e1s. Tambi\u00e9n contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. \u00a1Tenemos integraciones que te permiten tener una calculadora, una calculadora gr\u00e1fica, un diccionario, un comprobador de plagio, un mapamundi, una tabla peri\u00f3dica, un editor de c\u00f3digo y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho m\u00e1s! Estamos a\u00f1adiendo muchos m\u00e1s aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
    "cn": "\u8010\u535a\u4e50\u601d\u4f1a\u8ba9\u60a8\u7684\u6574\u4e2a\u5b66\u4e60\u4f53\u9a8c\u53d8\u5f97\u65e2\u7b80\u5355\uff0c\u53c8\u6709\u79e9\u5e8f\u3002\u9996\u5148\uff0c\u6211\u4eec\u4f1a\u7ed9\u4e88\u8bb8\u591a\u7f51\u7ad9\u8054\u7cfb\u3002\u60a8\u4e0d\u7528\u518d\u5728\u7f51\u7ad9\u4e4b\u95f4\u53cd\u590d\u9605\u89c8\u4e86\u3002\u6bd4\u5982\uff0c\u60a8\u53ef\u4ee5\u5728\u8010\u535a\u4e50\u601d\u5e73\u53f0\u4e0a\u8f7b\u677e\u5730\u8fde\u63a5\u50cfSchoology, Canvas, \u6216Google Classroom\u7b49\u5404\u79cd\u5b66\u4e60\u7f51\u7ad9\u3002\u5176\u6b21\uff0c\u60a8\u4e5f\u53ef\u4ee5\u5728\u8010\u535a\u4e50\u601d\u5e73\u53f0\u4e0a\u6709\u79e9\u5e8f\u5730\u5b66\u4e60\u3002\u60a8\u4e0d\u518d\u9700\u8981\u5c06\u6587\u6863\u3001\u8bba\u6587\u3001\u4f5c\u4e1a\u3001\u6559\u79d1\u4e66\u3001\u65f6\u95f4\u8868\u3001\u4e8b\u4ef6\u7b49\u6240\u6709\u4efb\u52a1\u644a\u5f97\u5230\u5904\u90fd\u662f\u4e86\u3002\u6240\u6709\u5143\u7d20\u90fd\u4f1a\u4e3a\u60a8\u6574\u7406\u6210\u4e00\u4e2a\u65b9\u4fbf\u5feb\u6377\u7684\u65b9\u5f0f\uff01\u60a8\u53ef\u4ee5\u5c06\u6240\u6709\u5b66\u6821\u9700\u8981\u7684\u5143\u7d20\u5168\u90fd\u6536\u96c6\u5728\u540c\u4e00\u4e2a\u5730\u65b9\u3002\u9664\u6b64\u4e4b\u5916\uff0c\u6211\u4eec\u4e5f\u5341\u5206\u7406\u89e3\u5b66\u4e60\u53ef\u80fd\u4f1a\u5f88\u67af\u71e5\u3002\u9488\u5bf9\u8fd9\u4e2a\uff0c\u6211\u4eec\u4e5f\u6709\u8bb8\u591a\u5de5\u5177\u53ef\u4ee5\u5e2e\u60a8\u5b66\u4e60\u3001\u6574\u7406\u8d44\u6599\u3001\u8ba9\u5b66\u4e60\u53d8\u5feb\u4e50\u3001\u540c\u65f6\u4e5f\u8ba9\u60a8\u4e13\u6ce8\u4e8e\u5b66\u4e60\uff01\u60a8\u53ef\u4ee5\u9009\u62e9\u4f7f\u7528\u6211\u4eec\u7684\u5b66\u4e60\u65f6\u949f\u3001\u8003\u8bd5\u5468\u8ba1\u5212\u8868\u3001\u7b49\u3002\u6211\u4eec\u4e5f\u6709\u8bb8\u591a\u6269\u5c55\u96c6\u6210\u53bb\u4e30\u5bcc\u60a8\u7684\u4f7f\u7528\u7ecf\u5386\u3002\u6211\u4eec\u5305\u62ec\u8ba1\u7b97\u673a\u96c6\u6210\u3001\u56fe\u8868\u8ba1\u7b97\u673a\u96c6\u6210\u3001\u5b57\u5178\u6269\u5c55\u3001\u6284\u88ad\u68c0\u67e5\u5668\u6269\u5c55\u3001\u4e16\u754c\u5730\u56fe\u3001\u5143\u7d20\u5468\u671f\u8868\u3001\u96c6\u6210\u4ee3\u7801\u7f16\u8f91\u5668\u3001\u53ef\u4ee5\u8de8\u7f16\u8f91\u5668\u7f16\u5199\u7684\u6587\u6863\u7f16\u8f91\u5668\u3001\u7b49\u8bb8\u591a\u5176\u4ed6\u7684\u5de5\u5177\uff01\u6211\u4eec\u4e5f\u4f1a\u572812\u670823\u53f7\u5373\u5c06\u53d1\u5e03\u7684\u7684\u7a33\u5b9a\u66f4\u65b0\u4e0a\u589e\u52a0\u66f4\u591a\u7684\u529f\u80fd\u9009\u9879\uff01",
    "tw": "\u8010\u535a\u6a02\u601d\u6703\u8b93\u60a8\u7684\u6574\u500b\u5b78\u7fd2\u9ad4\u9a57\u8b8a\u5f97\u65e2\u7c21\u55ae\uff0c\u53c8\u6709\u79e9\u5e8f\u3002\u9996\u5148\uff0c\u6211\u5011\u6703\u7d66\u4e88\u8a31\u591a\u7db2\u7ad9\u806f\u7e6b\u3002\u60a8\u4e0d\u7528\u518d\u5728\u7db2\u7ad9\u4e4b\u9593\u53cd\u590d\u95b1\u89bd\u4e86\u3002\u6bd4\u5982\uff0c\u60a8\u53ef\u4ee5\u5728\u8010\u535a\u6a02\u601d\u5e73\u53f0\u4e0a\u8f15\u9b06\u5730\u9023\u63a5\u50cfSchoology, Canvas, \u6216Google Classroom\u7b49\u5404\u7a2e\u5b78\u7fd2\u7db2\u7ad9\u3002\u5176\u6b21\uff0c\u60a8\u4e5f\u53ef\u4ee5\u5728\u8010\u535a\u6a02\u601d\u5e73\u53f0\u4e0a\u6709\u79e9\u5e8f\u5730\u5b78\u7fd2\u3002\u60a8\u4e0d\u518d\u9700\u8981\u5c07\u6587\u6a94\u3001\u8ad6\u6587\u3001\u4f5c\u696d\u3001\u6559\u79d1\u66f8\u3001\u6642\u9593\u8868\u3001\u4e8b\u4ef6\u7b49\u6240\u6709\u4efb\u52d9\u6524\u5f97\u5230\u8655\u90fd\u662f\u4e86\u3002\u6240\u6709\u5143\u7d20\u90fd\u6703\u70ba\u60a8\u6574\u7406\u6210\u4e00\u500b\u65b9\u4fbf\u5feb\u6377\u7684\u65b9\u5f0f\uff01\u60a8\u53ef\u4ee5\u5c07\u6240\u6709\u5b78\u6821\u9700\u8981\u7684\u5143\u7d20\u5168\u90fd\u6536\u96c6\u5728\u540c\u4e00\u500b\u5730\u65b9\u3002\u9664\u6b64\u4e4b\u5916\uff0c\u6211\u5011\u4e5f\u5341\u5206\u7406\u89e3\u5b78\u7fd2\u53ef\u80fd\u6703\u5f88\u67af\u71e5\u3002\u91dd\u5c0d\u9019\u500b\uff0c\u6211\u5011\u4e5f\u6709\u8a31\u591a\u5de5\u5177\u53ef\u4ee5\u5e6b\u60a8\u5b78\u7fd2\u3001\u6574\u7406\u8cc7\u6599\u3001\u8b93\u5b78\u7fd2\u8b8a\u5feb\u6a02\u3001\u540c\u6642\u4e5f\u8b93\u60a8\u5c08\u6ce8\u65bc\u5b78\u7fd2\uff01\u60a8\u53ef\u4ee5\u9078\u64c7\u4f7f\u7528\u6211\u5011\u7684\u5b78\u7fd2\u6642\u9418\u3001\u8003\u8a66\u9031\u8a08\u5283\u8868\u3001\u7b49\u3002\u6211\u5011\u4e5f\u6709\u8a31\u591a\u64f4\u5c55\u96c6\u6210\u53bb\u8c50\u5bcc\u60a8\u7684\u4f7f\u7528\u7d93\u6b77\u3002\u6211\u5011\u5305\u62ec\u8a08\u7b97\u6a5f\u96c6\u6210\u3001\u5716\u8868\u8a08\u7b97\u6a5f\u96c6\u6210\u3001\u5b57\u5178\u64f4\u5c55\u3001\u6284\u8972\u6aa2\u67e5\u5668\u64f4\u5c55\u3001\u4e16\u754c\u5730\u5716\u3001\u5143\u7d20\u9031\u671f\u8868\u3001\u96c6\u6210\u4ee3\u78bc\u7de8\u8f2f\u5668\u3001\u53ef\u4ee5\u8de8\u7de8\u8f2f\u5668\u7de8\u5beb\u7684\u6587\u6a94\u7de8\u8f2f\u5668\u3001\u7b49\u8a31\u591a\u5176\u4ed6\u7684\u5de5\u5177\uff01\u6211\u5011\u4e5f\u6703\u572812\u670823\u865f\u5373\u5c07\u767c\u5e03\u7684\u7684\u7a69\u5b9a\u66f4\u65b0\u4e0a\u589e\u52a0\u66f4\u591a\u7684\u529f\u80fd\u9078\u9805\uff01",
    "hk": "\u8010\u535a\u6a02\u601d\u6703\u8b93\u60a8\u7684\u6574\u500b\u5b78\u7fd2\u9ad4\u9a57\u8b8a\u5f97\u65e2\u7c21\u55ae\uff0c\u53c8\u6709\u79e9\u5e8f\u3002\u9996\u5148\uff0c\u6211\u5011\u6703\u7d66\u4e88\u8a31\u591a\u7db2\u7ad9\u806f\u7e6b\u3002\u60a8\u4e0d\u7528\u518d\u5728\u7db2\u7ad9\u4e4b\u9593\u53cd\u590d\u95b1\u89bd\u4e86\u3002\u6bd4\u5982\uff0c\u60a8\u53ef\u4ee5\u5728\u8010\u535a\u6a02\u601d\u5e73\u53f0\u4e0a\u8f15\u9b06\u5730\u9023\u63a5\u50cfSchoology, Canvas, \u6216Google Classroom\u7b49\u5404\u7a2e\u5b78\u7fd2\u7db2\u7ad9\u3002\u5176\u6b21\uff0c\u60a8\u4e5f\u53ef\u4ee5\u5728\u8010\u535a\u6a02\u601d\u5e73\u53f0\u4e0a\u6709\u79e9\u5e8f\u5730\u5b78\u7fd2\u3002\u60a8\u4e0d\u518d\u9700\u8981\u5c07\u6587\u6a94\u3001\u8ad6\u6587\u3001\u4f5c\u696d\u3001\u6559\u79d1\u66f8\u3001\u6642\u9593\u8868\u3001\u4e8b\u4ef6\u7b49\u6240\u6709\u4efb\u52d9\u6524\u5f97\u5230\u8655\u90fd\u662f\u4e86\u3002\u6240\u6709\u5143\u7d20\u90fd\u6703\u70ba\u60a8\u6574\u7406\u6210\u4e00\u500b\u65b9\u4fbf\u5feb\u6377\u7684\u65b9\u5f0f\uff01\u60a8\u53ef\u4ee5\u5c07\u6240\u6709\u5b78\u6821\u9700\u8981\u7684\u5143\u7d20\u5168\u90fd\u6536\u96c6\u5728\u540c\u4e00\u500b\u5730\u65b9\u3002\u9664\u6b64\u4e4b\u5916\uff0c\u6211\u5011\u4e5f\u5341\u5206\u7406\u89e3\u5b78\u7fd2\u53ef\u80fd\u6703\u5f88\u67af\u71e5\u3002\u91dd\u5c0d\u9019\u500b\uff0c\u6211\u5011\u4e5f\u6709\u8a31\u591a\u5de5\u5177\u53ef\u4ee5\u5e6b\u60a8\u5b78\u7fd2\u3001\u6574\u7406\u8cc7\u6599\u3001\u8b93\u5b78\u7fd2\u8b8a\u5feb\u6a02\u3001\u540c\u6642\u4e5f\u8b93\u60a8\u5c08\u6ce8\u65bc\u5b78\u7fd2\uff01\u60a8\u53ef\u4ee5\u9078\u64c7\u4f7f\u7528\u6211\u5011\u7684\u5b78\u7fd2\u6642\u9418\u3001\u8003\u8a66\u9031\u8a08\u5283\u8868\u3001\u7b49\u3002\u6211\u5011\u4e5f\u6709\u8a31\u591a\u64f4\u5c55\u96c6\u6210\u53bb\u8c50\u5bcc\u60a8\u7684\u4f7f\u7528\u7d93\u6b77\u3002\u6211\u5011\u5305\u62ec\u8a08\u7b97\u6a5f\u96c6\u6210\u3001\u5716\u8868\u8a08\u7b97\u6a5f\u96c6\u6210\u3001\u5b57\u5178\u64f4\u5c55\u3001\u6284\u8972\u6aa2\u67e5\u5668\u64f4\u5c55\u3001\u4e16\u754c\u5730\u5716\u3001\u5143\u7d20\u9031\u671f\u8868\u3001\u96c6\u6210\u4ee3\u78bc\u7de8\u8f2f\u5668\u3001\u53ef\u4ee5\u8de8\u7de8\u8f2f\u5668\u7de8\u5beb\u7684\u6587\u6a94\u7de8\u8f2f\u5668\u3001\u7b49\u8a31\u591a\u5176\u4ed6\u7684\u5de5\u5177\uff01\u6211\u5011\u4e5f\u6703\u572812\u670823\u865f\u5373\u5c07\u767c\u5e03\u7684\u7684\u7a69\u5b9a\u66f4\u65b0\u4e0a\u589e\u52a0\u66f4\u591a\u7684\u529f\u80fd\u9078\u9805\uff01",
    "mo": "\u8010\u535a\u6a02\u601d\u6703\u8b93\u60a8\u7684\u6574\u500b\u5b78\u7fd2\u9ad4\u9a57\u8b8a\u5f97\u65e2\u7c21\u55ae\uff0c\u53c8\u6709\u79e9\u5e8f\u3002\u9996\u5148\uff0c\u6211\u5011\u6703\u7d66\u4e88\u8a31\u591a\u7db2\u7ad9\u806f\u7e6b\u3002\u60a8\u4e0d\u7528\u518d\u5728\u7db2\u7ad9\u4e4b\u9593\u53cd\u590d\u95b1\u89bd\u4e86\u3002\u6bd4\u5982\uff0c\u60a8\u53ef\u4ee5\u5728\u8010\u535a\u6a02\u601d\u5e73\u53f0\u4e0a\u8f15\u9b06\u5730\u9023\u63a5\u50cfSchoology, Canvas, \u6216Google Classroom\u7b49\u5404\u7a2e\u5b78\u7fd2\u7db2\u7ad9\u3002\u5176\u6b21\uff0c\u60a8\u4e5f\u53ef\u4ee5\u5728\u8010\u535a\u6a02\u601d\u5e73\u53f0\u4e0a\u6709\u79e9\u5e8f\u5730\u5b78\u7fd2\u3002\u60a8\u4e0d\u518d\u9700\u8981\u5c07\u6587\u6a94\u3001\u8ad6\u6587\u3001\u4f5c\u696d\u3001\u6559\u79d1\u66f8\u3001\u6642\u9593\u8868\u3001\u4e8b\u4ef6\u7b49\u6240\u6709\u4efb\u52d9\u6524\u5f97\u5230\u8655\u90fd\u662f\u4e86\u3002\u6240\u6709\u5143\u7d20\u90fd\u6703\u70ba\u60a8\u6574\u7406\u6210\u4e00\u500b\u65b9\u4fbf\u5feb\u6377\u7684\u65b9\u5f0f\uff01\u60a8\u53ef\u4ee5\u5c07\u6240\u6709\u5b78\u6821\u9700\u8981\u7684\u5143\u7d20\u5168\u90fd\u6536\u96c6\u5728\u540c\u4e00\u500b\u5730\u65b9\u3002\u9664\u6b64\u4e4b\u5916\uff0c\u6211\u5011\u4e5f\u5341\u5206\u7406\u89e3\u5b78\u7fd2\u53ef\u80fd\u6703\u5f88\u67af\u71e5\u3002\u91dd\u5c0d\u9019\u500b\uff0c\u6211\u5011\u4e5f\u6709\u8a31\u591a\u5de5\u5177\u53ef\u4ee5\u5e6b\u60a8\u5b78\u7fd2\u3001\u6574\u7406\u8cc7\u6599\u3001\u8b93\u5b78\u7fd2\u8b8a\u5feb\u6a02\u3001\u540c\u6642\u4e5f\u8b93\u60a8\u5c08\u6ce8\u65bc\u5b78\u7fd2\uff01\u60a8\u53ef\u4ee5\u9078\u64c7\u4f7f\u7528\u6211\u5011\u7684\u5b78\u7fd2\u6642\u9418\u3001\u8003\u8a66\u9031\u8a08\u5283\u8868\u3001\u7b49\u3002\u6211\u5011\u4e5f\u6709\u8a31\u591a\u64f4\u5c55\u96c6\u6210\u53bb\u8c50\u5bcc\u60a8\u7684\u4f7f\u7528\u7d93\u6b77\u3002\u6211\u5011\u5305\u62ec\u8a08\u7b97\u6a5f\u96c6\u6210\u3001\u5716\u8868\u8a08\u7b97\u6a5f\u96c6\u6210\u3001\u5b57\u5178\u64f4\u5c55\u3001\u6284\u8972\u6aa2\u67e5\u5668\u64f4\u5c55\u3001\u4e16\u754c\u5730\u5716\u3001\u5143\u7d20\u9031\u671f\u8868\u3001\u96c6\u6210\u4ee3\u78bc\u7de8\u8f2f\u5668\u3001\u53ef\u4ee5\u8de8\u7de8\u8f2f\u5668\u7de8\u5beb\u7684\u6587\u6a94\u7de8\u8f2f\u5668\u3001\u7b49\u8a31\u591a\u5176\u4ed6\u7684\u5de5\u5177\uff01\u6211\u5011\u4e5f\u6703\u572812\u670823\u865f\u5373\u5c07\u767c\u5e03\u7684\u7684\u7a69\u5b9a\u66f4\u65b0\u4e0a\u589e\u52a0\u66f4\u591a\u7684\u529f\u80fd\u9078\u9805\uff01",
    "kr": "\ub124\ubdf8\ub7ec\uc2a4 \ub97c \uc0ac\uc6a9\ud558\uba74 \uc804\uccb4 \ud559\uc2b5 \uacbd\ud5d8\uc744 \uccb4\uacc4\uc801\uc774\uace0 \uac04\ub2e8\ud558\uac8c \ub9cc\ub4e4 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \uccab\uc9f8, \uc6b0\ub9ac\ub294 \ub9ce\uc740 \uc5f0\uacb0\uc744 \uc81c\uacf5\ud569\ub2c8\ub2e4. \ub354 \uc774\uc0c1 \uc6f9\uc0ac\uc774\ud2b8 \uac04\uc5d0 \uc804\ud658\ud560 \ud544\uc694\uac00 \uc5c6\uc2b5\ub2c8\ub2e4. \ub124\ubdf8\ub7ec\uc2a4\uc5d0 \uc5f0\uacb0\ub41c Schoology, Google \ud074\ub798\uc2a4\ub8f8 \ubc0f Canvas \uacc4\uc815\uc744 \uc5f0\uacb0\ud558\uc5ec \uc27d\uac8c \uc561\uc138\uc2a4\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \ub124\ubdf8\ub7ec\uc2a4\ub85c \uc815\ub9ac\ub97c \uc720\uc9c0\ud560 \uc218\ub3c4 \uc788\uc2b5\ub2c8\ub2e4. \uc11c\ub958, \ubb38\uc11c, \uacfc\uc81c, \uad50\uacfc\uc11c, \ub2ec\ub825 \ubc0f \uc774\ubca4\ud2b8\ub97c \uc5ec\uae30\uc800\uae30\uc5d0 \ub458 \ud544\uc694\uac00 \uc5c6\uc2b5\ub2c8\ub2e4. \ubaa8\ub4e0 \uac83\uc774 \uc0ac\uc6a9\ud558\uae30 \uc26c\uc6b4 \ubc29\uc2dd\uc73c\ub85c \uad6c\uc131\ub418\uc5b4 \uc788\uc2b5\ub2c8\ub2e4! \ud559\uad50\uc5d0 \ud544\uc694\ud55c \ubaa8\ub4e0 \uac83\uc744 \ud55c \uacf3\uc5d0\uc11c \ubc1b\uc744 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \ub610\ud55c \uc6b0\ub9ac\ub294 \uacf5\ubd80\uc640 \ud559\uc2b5\uc774 \uc5b4\ub824\uc6b8 \uc218 \uc788\uc74c\uc744 \uc774\ud574\ud569\ub2c8\ub2e4. \ud559\uc2b5\uc744 \uc815\ub9ac\ud558\uace0, \uc790\ub8cc\ub97c \uc815\ub9ac\ud558\uace0, \ud559\uc2b5\uc744 \uc7ac\ubbf8\uc788\uac8c \ub9cc\ub4e4\uace0, \uc9d1\uc911\ud560 \uc218 \uc788\ub294 \ub3c4\uad6c\uac00 \uc788\uc2b5\ub2c8\ub2e4! \ud559\uc2b5 \ud0c0\uc774\uba38, \uc2dc\ud5d8 \uac80\ud1a0 \uacc4\ud68d \ub4f1\uc744 \uc0ac\uc6a9\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \uacbd\ud5d8\uc744 \ud48d\ubd80\ud558\uac8c \ud558\uae30 \uc704\ud574 \ub9ce\uc740 \ud655\uc7a5 \ubc0f \ud1b5\ud569\uc774 \uc788\uc2b5\ub2c8\ub2e4. \uacc4\uc0b0\uae30 \ud1b5\ud569, \uadf8\ub798\ud504 \uacc4\uc0b0\uae30, \uc0ac\uc804, \ud45c\uc808 \uac80\uc0ac\uae30, \uc138\uacc4 \uc9c0\ub3c4, \uc8fc\uae30\uc728\ud45c, \ub0b4\uc7a5 IDE(\ucf54\ub4dc \ud3b8\uc9d1\uae30) \ubc0f \ubb38\uc11c \ud3b8\uc9d1\uae30(Word \ub610\ub294 Google \ubb38\uc11c\ub97c \ud3b8\uc9d1\ud560 \uc218 \uc788\uc74c) \ubc0f \ub9ce\uc740 \uae30\ub2a5\uc774 \uc788\uc2b5\ub2c8\ub2e4. \ub354! 12\uc6d4 23\uc77c \uacf5\uac1c \ubc84\uc804 \ub9b4\ub9ac\uc2a4\uc5d0 \ub354 \ub9ce\uc740 \uae30\ub2a5\uc744 \ucd94\uac00\ud558\uace0 \uc788\uc2b5\ub2c8\ub2e4."
  },
  "Login": {
    "cn": "\u767b\u5f55"
  },
  "Signup": {
    "cn": "\u6ce8\u518c"
  },
  "Sign Up": {
    "cn": "\u6ce8\u518c"
  },
  "Launch Nebulus": {
    "cn": "\u542f\u52a8\u8010\u535a\u4e50\u601d"
  },
  "Watch Our Event": {
    "cn": "\u89c2\u770b\u6211\u4eec\u7684\u6d3b\u52a8"
  },
  "Get Started": {
    "cn": "\u5f00\u59cb\u4f7f\u7528\uff01"
  },
  "Learning, All In One": {
    "us": "Learning, All In One",
    "uk": "Learning, All In One",
    "au": "Learning, All In One",
    "es": "Todo tu aprendizaje en un sitio",
    "mx": "Todo tu aprendizaje en un sitio",
    "cr": "Todo tu aprendizaje en un sitio",
    "cu": "Todo tu aprendizaje en un sitio",
    "co": "Todo tu aprendizaje en un sitio",
    "ar": "Todo tu aprendizaje en un sitio",
    "cn": "\u6709\u8da3\u3001\u5168\u9762\u5730\u5b66\u4e60"
  },
  "Connect all of Learning": {
    "us": "Connect all of Learning",
    "uk": "Connect all of Learning",
    "au": "Connect all of Learning",
    "es": "Conecta todo tu aprendizaje",
    "mx": "Conecta todo tu aprendizaje",
    "cr": "Conecta todo tu aprendizaje",
    "cu": "Conecta todo tu aprendizaje",
    "co": "Conecta todo tu aprendizaje",
    "ar": "Conecta todo tu aprendizaje",
    "cn": "\u8fde\u63a5\u6240\u6709\u7684\u5b66\u4e60\u65b9\u5f0f"
  },
  "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.": {
    "us": "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.",
    "uk": "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.",
    "au": "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.",
    "es": "No cambies m\u00e1s entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
    "mx": "No cambies m\u00e1s entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
    "cr": "No cambies m\u00e1s entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
    "cu": "No cambies m\u00e1s entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
    "co": "No cambies m\u00e1s entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
    "ar": "No cambies m\u00e1s entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
    "cn": "\u60a8\u4e0d\u9700\u8981\u7ee7\u7eed\u5728\u7f51\u7ad9\u4e4b\u95f4\u5207\u6362\u3002\u5c06\u60a8\u7684Schoology. Google Classroom, \u4e0e Canvas\u8d26\u6237\u5168\u90e8\u8fde\u63a5\u5230\u8010\u535a\u4e50\u601d\u5c31\u53ef\u4ee5\u4e86\u3002"
  },
  "Organize your Learning Experience": {
    "us": "Organize your learning experience",
    "uk": "Organize your learning experience",
    "au": "Organize your learning experience",
    "es": "Organiza tu experiencia de aprendizaje",
    "mx": "Organiza tu experiencia de aprendizaje",
    "cr": "Organiza tu experiencia de aprendizaje",
    "cu": "Organiza tu experiencia de aprendizaje",
    "co": "Organiza tu experiencia de aprendizaje",
    "ar": "Organiza tu experiencia de aprendizaje",
    "cn": "\u89c4\u6574\u60a8\u7684\u5b66\u4e60\u7ecf\u5386"
  },
  "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!": {
    "us": "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!",
    "uk": "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!",
    "au": "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!",
    "es": "Con N\u00e9bulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. \u00a1Con N\u00e9bulus, todo est\u00e1 organizado para ti de manera f\u00e1cil de usar!",
    "mx": "Con N\u00e9bulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. \u00a1Con N\u00e9bulus, todo est\u00e1 organizado para ti de manera f\u00e1cil de usar!",
    "cr": "Con N\u00e9bulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. \u00a1Con N\u00e9bulus, todo est\u00e1 organizado para ti de manera f\u00e1cil de usar!",
    "cu": "Con N\u00e9bulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. \u00a1Con N\u00e9bulus, todo est\u00e1 organizado para ti de manera f\u00e1cil de usar!",
    "co": "Con N\u00e9bulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. \u00a1Con N\u00e9bulus, todo est\u00e1 organizado para ti de manera f\u00e1cil de usar!",
    "ar": "Con N\u00e9bulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. \u00a1Con N\u00e9bulus, todo est\u00e1 organizado para ti de manera f\u00e1cil de usar!",
    "cn": "\u6709\u4e86\u8010\u535a\u4e50\u601d\uff0c\u60a8\u7684\u8bba\u6587\u3001\u6587\u6863\u3001\u4f5c\u4e1a\u3001\u6559\u79d1\u4e66\u548c\u6d3b\u52a8\u5c31\u4e0d\u5fc5\u5230\u5904\u4e71\u7a9c\u4e86\u3002 \u4f7f\u7528 \u8010\u535a\u4e50\u601d\uff0c\u4e00\u5207\u90fd\u4ee5\u6613\u4e8e\u4f7f\u7528\u7684\u65b9\u5f0f\u4e3a\u60a8\u5b89\u6392\u59a5\u5f53\uff01"
  },
  "Make Learning Easier": {
    "us": "Make Learning Easier",
    "uk": "Make Learning Easier",
    "au": "Make Learning Easier",
    "es": "Haz tu aprendizaje m\u00e1s f\u00e1cil",
    "mx": "Haz tu aprendizaje m\u00e1s f\u00e1cil",
    "cr": "Haz tu aprendizaje m\u00e1s f\u00e1cil",
    "cu": "Haz tu aprendizaje m\u00e1s f\u00e1cil",
    "co": "Haz tu aprendizaje m\u00e1s f\u00e1cil",
    "ar": "Haz tu aprendizaje m\u00e1s f\u00e1cil",
    "cn": "\u8ba9\u5b66\u4e60\u66f4\u7b80\u5355\u548c\u8f7b\u677e"
  },
  "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!": {
    "us": "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!",
    "uk": "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!",
    "au": "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!",
    "es": "\u00a1Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n!",
    "mx": "\u00a1Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n!",
    "cr": "\u00a1Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n!",
    "cu": "\u00a1Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n!",
    "co": "\u00a1Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n!",
    "ar": "\u00a1Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentraci\u00f3n!",
    "cn": "\u6211\u4eec\u62e5\u6709\u53ef\u4ee5\u8bb8\u591a\u5de5\u5177\u53ef\u4ee5\u5e2e\u52a9\u60a8\u5b66\u4e60\uff0c\u6574\u7406\u8d44\u6599\uff0c\u8ba9\u5b66\u4e60\u53d8\u5f97\u6709\u8da3\uff0c\u5e76\u4e14\u5e2e\u52a9\u60a8\u4fdd\u6301\u4e13\u6ce8\uff01"
  },
  "Start Now!": {
    "us": "Start Now!",
    "uk": "Start Now!",
    "au": "Start Now!",
    "es": "\u00a1Comienza ahora!",
    "mx": "\u00a1Comienza ahora!",
    "cr": "\u00a1Comienza ahora!",
    "cu": "\u00a1Comienza ahora!",
    "co": "\u00a1Comienza ahora!",
    "ar": "\u00a1Comienza ahora!",
    "cn": "\u5f00\u59cb\u4f7f\u7528\uff01"
  },
  "About": {
    "cn": "\u5173\u4e8e"
  },
  "Pricing": {
    "cn": "\u4ef7\u94b1"
  },
  "Change Language": {
    "cn": "\u6539\u53d8\u8bed\u8a00"
  },
  "With Nebulus, have your whole learning experience": {
    "cn": "\u8010\u535a\u4e50\u601d\u4f1a\u8ba9\u60a8\u7684\u5b66\u4e60\u7ecf\u5386\u65e2\u6709"
  },
  "organized": {
    "cn": "\u79e9\u5e8f"
  },
  "and": {
    "cn": "\u3001\u53c8"
  },
  "simple": {
    "cn": "\u7b80\u5355\u65b9\u4fbf"
  },
  "All it takes is one": {
    "cn": "\u60a8\u6240\u9700\u7684\u4ec5\u4ec5\u662f\u4e00\u4e2a"
  },
  "Nebulus Account": {
    "cn": "\u8010\u535a\u4e50\u601d\u8d26\u53f7"
  },
  "New to Nebulus?": {
    "cn": "\u65b0\u624b\u6307\u5357?"
  },
  "Forgot password?": {
    "cn": "\u5fd8\u8bb0\u5bc6\u7801\uff1f"
  },
  "Reset": {
    "cn": "\u91cd\u5236"
  },
  "Or, Sign in with Your Apps:": {
    "cn": "\u6216\u8005\uff0c\u4f7f\u7528\u5176\u5b83\u5e94\u7528\u767b\u5f55\uff1a"
  },
  "Sign up Now": {
    "cn": "\u73b0\u5728\u6ce8\u518c"
  },
  "Password": {
    "cn": "\u5bc6\u7801"
  },
  "Username": {
    "cn": "\u7528\u6237\u540d"
  },
  "Email": {
    "cn": "\u90ae\u7bb1"
  },
  "Existing Member?": {
    "cn": "\u5df2\u6ce8\u518c\u8d26\u6237\uff1f"
  },
  "Prepare for a brighter future in your education with Nebulus!  It's free and it always will be.": {
    "cn": "\u51c6\u5907\u597d\u4e0e\u8010\u535a\u4e50\u601d\u4e00\u8d77\u5728\u60a8\u7684\u5b66\u4e60\u8fc7\u7a0b\u4e2d\u5f00\u542f\u4e00\u4e2a\u66f4\u7f8e\u597d\u7684\u672a\u6765\uff01"
  },
  "Restart": {
    "cn": "\u91cd\u65b0\u8f93\u5165"
  },
  "Next": {
    "cn": "\u4e0b\u4e00\u6b65"
  },
  "Previous": {
    "cn": "\u524d\u4e00\u6b65"
  },
  "Join": {
    "cn": "\u5f00\u59cb\u7528\u8010\u535a\u4e50\u601d\uff01"
  },
  "Confirm Password": {
    "cn": "\u786e\u8ba4\u5bc6\u7801"
  },
  "Welcome to Nebulus! Please enter an Email!": {
    "cn": " \u6b22\u8fce\u6765\u5230\u8010\u535a\u4e50\u601d\uff01\u8bf7\u8f93\u5165\u7528\u6237\u540d\u3002"
  },
  "Please enter a Username!": {
    "cn": "\u8bf7\u8f93\u5165\u7528\u6237\u540d\u3002"
  },
  "Please enter a password!": {
    "cn": "\u8bf7\u8f93\u5165\u5bc6\u7801\uff01"
  },
  "Please confirm your password!": {
    "cn": "\u8bf7\u786e\u8ba4\u60a8\u7684\u5bc6\u7801\uff01"
  }
}


def getText(query):
    try:
        return dictionary[query][session["global"]]
    except KeyError:
        return query


def getAssignment(assignment_id: str) -> Assignment:
    assignment = Assignment.objects(id=assignment_id).first()
    return assignment


def getNebulusDocument(document_id: str) -> NebulusDocument:
    document = NebulusDocument.objects(id=document_id).first()
    return document


def getEvent(event_id: str) -> Event:
    event = Event.objects(pk=event_id).first()
    return event


def getGrades(grades_id: str) -> Grades:
    grades = Grades.objects(pk=grades_id).first()
    return grades


def getDocumentFile(document_file_id: str) -> DocumentFile:
    document_file = DocumentFile.objects(pk=document_file_id).first()
    return document_file


def getFolder(folder_id: str) -> Folder:
    folder = Folder.objects(pk=folder_id).first()
    return folder


def get_user_courses(user_id: str) -> list[Course]:
    user = find_user(pk=user_id)
    return Course.objects(authorizedUsers=user)


def get_user_docs(user_id: str) -> list[NebulusDocument]:
    user = find_user(pk=user_id)
    return NebulusDocument.objects(authorizedUsers=user)


def search_user(query: str, ignore_id: str = None) -> list[User]:
    if ignore_id:
        return User.objects(username__istartswith=query, id__ne=ignore_id).only(
            "id", "username", "email", "avatar", "_cls"
        )[:10]
    else:
        return User.objects(username__istartswith=query).only(
            "id", "username", "email", "avatar", "_cls"
        )[:10]
    # return User.objects.filter(username__contains=query)._query


def search_within_course(query: str, course_id: str):
    assignments = Assignment.objects(course_id=course_id, title__contains=query)
    events = Event.objects(course_id=course_id, title__contains=query)
    document_file = DocumentFile.objects(course_id=course_id, title__contains=query)


def find_courses(_id: str):
    course = Course.objects(pk=_id)
    if not course:
        raise KeyError("Course not found")
    return course[0]


def find_user(**kwargs) -> User | None:
    data = {k: v for k, v in kwargs.items() if v is not None}
    user = User.objects(**data).first()
    if not user:
        raise KeyError("User not found")

    return user


def find_folder(**kwargs) -> Folder | None:
    folder = Folder.objects(**kwargs).first()
    if not folder:
        print(folder)
        raise KeyError("Folder not found")
    return folder


def find_document(**kwargs) -> Document | None:
    document = DocumentFile.objects(**kwargs).first()
    if not document:
        print(document)
        raise KeyError("User not found")
    return document


def getSchoology(**kwargs) -> list[Schoology] | None:
    try:
        return find_user(**kwargs).schoology
    except KeyError:
        return


def getClassroom(
        userID: str = None, username: str = None, email: str = None
) -> GoogleClassroom:
    return find_user(id=userID, username=username, email=email).gclassroom


def getSpotify(userID: str = None, username: str = None, email: str = None) -> Spotify:
    return find_user(id=userID, username=username, email=email).spotify


def getSpotifyCache(
        userID: str = None, username: str = None, email: str = None
) -> Spotify | None:
    try:
        return find_user(
            id=userID, username=username, email=email
        ).spotify.Spotify_cache
    except:
        return None


def checkSchoology(_id: int):
    user = find_user(id=_id)
    return str(user and user.schoology).lower()


def check_type(o):
    try:
        a = find_folder(**o)
        if a is None:
            return "document"
        else:
            return "folder"
    except:
        return "document"


def check_signin(email, password):
    try:
        user = find_user(email=email)
    except KeyError:
        return False

    return valid_password(user.password, password)


def get_announcement(announcement_id: str) -> Announcement:
    announcement = Announcement.objects(pk=announcement_id).first()
    return announcement


def get_folders(parent_id: int = None, course_id: int = None) -> list[Folder]:
    if not parent_id and not course_id:
        raise ValueError("Must provide either parent_id or course_id")

    if course_id:
        return find_courses(course_id).folders
    else:
        return find_folder(id=parent_id).subfolders


def sortByDate(obj):
    return obj.date.date() if obj._cls == "Event" else obj.due.date()


def sortByDateTime(obj):
    return obj.date if obj._cls == "Event" else obj.due


def sort_course_events(user_id: str, course_id: int):
    courses = get_user_courses(user_id)
    course = None
    for i in courses:
        if str(i.id) == str(course_id):
            course = i
            break
    courses = [course]

    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain, groupby

    events_assessments_assignments = list(chain(events, assignments, assessments))
    sorted_events = sorted(
        events_assessments_assignments, key=lambda obj: sortByDateTime(obj)
    )
    dates = dict(
        {
            key: list(result)
            for key, result in groupby(
            sorted_events, key=lambda obj: sortByDateTime(obj)
        )
        }
    )

    sorted_announcements = sorted(announcements, key=lambda obj: obj.date)
    announcements = dict(
        reversed(
            list(
                {
                    key: list(result)
                    for key, result in groupby(
                    sorted_announcements, key=lambda obj: obj.date.date()
                )
                }.items()
            )
        )
    )

    return [announcements, dates]


def sort_user_events(user_id: str, maxDays=5, maxEvents=16):
    courses = get_user_courses(user_id)
    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain, groupby

    events_assessments_assignments = list(chain(events, assignments, assessments))
    sorted_events = reversed(
        sorted(
            events_assessments_assignments[:maxEvents],
            key=lambda obj: sortByDateTime(obj),
        )
    )

    dates = dict(
        {
            key: list(result)
            for key, result in groupby(
            sorted_events, key=lambda obj: sortByDateTime(obj)
        )
        }
    )

    sorted_announcements = sorted(announcements, key=lambda obj: obj.date)
    announcements = dict(
        reversed(
            list(
                {
                    key: list(result)
                    for key, result in groupby(
                    sorted_announcements, key=lambda obj: obj.date.date()
                )
                }.items()
            )[-maxDays:]
        )
    )

    return [announcements, dates]

    # events_assessments_assignments = events | assignments | assessments


def unsorted_user_events(user_id: str) -> list[list]:
    courses = get_user_courses(user_id)
    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain

    events_assessments_assignments = list(chain(events, assignments, assessments))
    announcements = list(reversed(announcements))
    return [
        announcements,
        sorted(events_assessments_assignments, key=lambda obj: sortByDateTime(obj)),
    ]


def getSchoologyAuth(user_id) -> schoolopy.Schoology | None:
    schoology = getSchoology(id=user_id)
    if not schoology:
        return

    schoology = schoology[0]
    request_token = schoology.Schoology_request_token
    request_token_secret = schoology.Schoology_request_secret
    access_token = schoology.Schoology_access_token
    access_token_secret = schoology.Schoology_access_secret
    link = schoology.schoologyDomain
    key = schoology.apikey
    secret = schoology.apisecret
    auth = schoolopy.Auth(
        key,
        secret,
        domain=link,
        three_legged=True,
        request_token=request_token,
        request_token_secret=request_token_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    auth.authorize()
    sc = schoolopy.Schoology(auth)
    sc.limit = 5

    return sc


def check_signup_user(username) -> str:
    if User.objects(username=username):
        return "false"
    return "true"


def check_signup_email(email) -> str:
    if User.objects(email=email):
        return "false"
    return "true"


def check_duplicate_schoology(schoology_email) -> str:
    if User.objects(schoology__schoologyEmail=schoology_email):
        return "true"
    return "false"


def getChat(chat_id: str):
    chat = Chat.objects.get(pk=chat_id)
    if not chat:
        raise KeyError("Invalid Chat ID")

    return chat


def getPlanner(user_id: str):
    planner = find_user(id=user_id).planner
    if not planner:
        return {}

    return {
        "name": planner.name,
        "saveData": planner.saveData,
        "periods": planner.periods,
        "lastEdited": planner.lastEdited,
    }


def getDocument(document_id: str):  # Nebulus Document
    doc = NebulusDocument.objects(pk=document_id)
    if not doc:
        raise KeyError("Invalid Document ID")
    return doc


def search(keyword: str, username: str):
    user = User.objects(username=username).first()
    users = search_user(keyword)
    pipeline1 = [
        {"$match": {"title": {"$regex": f"^{keyword}", "$options": "i"}}},
        {
            "$lookup": {
                "from": Course._get_collection_name(),
                "localField": "course",
                "foreignField": "_id",
                "as": "course",
            }
        },
        {"$match": {"course.authorizedUsers": user.pk}},
        {"$project": {"title": 1, "_id": 1, "_cls": 1}},
    ]
    courses = Course.objects(Q(authorizedUsers=user.id) & Q(name__istartswith=keyword))[
              :10
              ]
    chats = Chat.objects(Q(owner=user.id) & Q(title__istartswith=keyword))[:10]
    NebulusDocuments = NebulusDocument.objects(
        Q(authorizedUsers=user.id) & Q(name__istartswith=keyword)
    )[:10]

    events = list(Event.objects().aggregate(pipeline1))
    assignments = list(Assignment.objects().aggregate(pipeline1))
    announcements = list(Announcement.objects().aggregate(pipeline1))
    documents = list(DocumentFile.objects.aggregate(pipeline1))
    return (
        courses,
        documents,
        chats,
        events,
        assignments,
        announcements,
        NebulusDocuments,
        users,
    )


def search_course(keyword: str, course: str):
    course = Course.objects(id=course).first()
    pipeline1 = [
        {"$match": {"title": {"$regex": f"^{keyword}", "$options": "i"}}},
        {
            "$lookup": {
                "from": Course._get_collection_name(),
                "localField": "course",
                "foreignField": "_id",
                "as": "course",
            }
        },
        {"$match": {"course.id": course}},
        {"$project": {"title": 1, "_id": 1, "_cls": 1}},
    ]

    events = list(Event.objects().aggregate(pipeline1))
    assignments = list(Assignment.objects().aggregate(pipeline1))
    announcements = list(Announcement.objects().aggregate(pipeline1))
    documents = list(DocumentFile.objects.aggregate(pipeline1))
    return (
        documents,
        events,
        assignments,
        announcements,
        # NebulusDocuments,
    )


def getUserChats(user_id, required_fields: list):
    chats = Chat.objects(members__user=user_id).only(*required_fields)
    return chats


def loadChats(user_id: str, current_index, initial_amount, required_fields):
    chats = json.loads(getUserChats(user_id, required_fields).to_json())

    chats = sorted(chats, key=lambda x: x["lastEdited"]["$date"], reverse=True)

    if len(chats) < current_index + initial_amount:
        initial_amount = len(chats) - current_index

    chats = chats[current_index: (current_index + initial_amount)]
    for chat in chats:
        if len(chat["members"]) == 2:
            for x, member in enumerate(chat["members"]):
                chat["members"][x]["user"] = json.loads(
                    User.objects.only(
                        "id", "chatProfile", "username", "avatar.avatar_url"
                    )
                    .get(pk=member["user"])
                    .to_json()
                )
                chat["members"][x]["unread"] = str(chat["members"][x]["unread"])
            chat["owner"] = list(
                filter(lambda x: x["user"]["_id"] == chat["owner"], chat["members"])
            )[0]

    print(chats)
    return chats


def get_friends(user_id):
    user = find_user(pk=user_id)
    try:
        friends = user.chatProfile.friends
    except:
        friends = None
    return friends


def get_blocks(user_id):
    user = find_user(pk=user_id)
    try:
        blocked = user.chatProfile.blocked
    except:
        blocked = None
    return blocked


def get_user_notepad(user):
    user = find_user(pk=user)
    try:
        # print(user.notepad)
        notepad = dict(user.notepad.data)
    except Exception as e:

        print(e)
        notepad = {}
    return notepad
