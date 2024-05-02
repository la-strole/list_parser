PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE advertisement (
        id INTEGER PRIMARY KEY,
        image_href VARCHAR(255) NOT NULL,
        title TEXT NOT NULL,
        price_value INTEGER NOT NULL,
        currancy CHARACTER(3) NOT NULL,   
        description TEXT NOT NULL,
        date_posted TEXT NOT NULL,
        date_updated TEXT DEFAULT NULL,
        location VARCHAR(255) NOT NULL,
        agent_status BOOLEAN NOT NULL,
        user_link VARCHAR(255) NOT NULL,   
        appliances TEXT DEFAULT NULL,
        garage BOOLEAN DEFAULT NULL,
        rooms_count INTEGER DEFAULT NULL,
        toilet_count INTEGER DEFAULT 1,
        utility_bills_included BOOLEAN DEFAULT NULL,
        furniture TEXT DEFAULT NULL,
        children_allowed BOOLEAN DEFAULT NULL,
        animals_allowed BOOLEAN DEFAULT NULL,
        total_area INTEGER DEFAULT NULL,
        land_area INTEGER DEFAULT NULL,
        prepayment TEXT DEFAULT NULL,
        appartment_state TEXT DEFAULT NULL,
        type VARCHAR(50) DEFAULT NULL,
        building_type VARCHAR(50) DEFAULT NULL,
        facilities TEXT DEFAULT NULL,
        floors_count INTEGER DEFAULT 1,
        district VARCHAR(50) DEFAULT NULL,
        price_amd INTEGER NOT NULL
);
INSERT INTO advertisement VALUES(16879582,'https://s.list.am/f/974/57252974.webp','Одноэтажный каменный дом на ул. Амо Сагияна в Арабкирe, 84 кв.м., евроремонт',260000,'AMD','Տրվում է վարձով 3 սենյականոց սեփական տան 2 սենյակը։ 3 րդը փակ է լինելու։ Կոմիտասում, Սլավոնական համալսարանի մոտ։ Առկա է նաև կահույք և տեխնիկա։ Նկարները համապատասխանում են։ Baxi ջեռուցման համակարգով, տաք հատակ։ Շատ տաք ու մաքուր տուն է։ Կարելի է նաև օրավաձով Սեփականատեր։ Զանգահարեք միայն վատսապով կամ վայբերով Сдается частный дом в аренду, В комитасе. В районе Славянского университета. 2 спальня (вторая спальня будет закрыта), 1 большой зал, 1 ванная комната, 1 кухня и прихожая. Мебель и бытовая техника. Фотографии соответствуют. Система отопления Baxi, теплый пол. Очень тёплый и чистый дом. Собственник. Можно и посуточно Без комиссии. For rent home In avenue Komitas, Near the Slavic University. 2 bedroom (the second bedroom will be closed), 1 big holl 1 bathroom, 1 kitchen and hallway. There is also furniture and appliances. The photos match. Baxi heating system, underfloor heating. Very warm and clean house. Conditions and price are changeable, I will also hear your offer. It is also possible for a day Owner.','2021-10-26T07:38:02+00:00','2024-04-30T21:55:00','Улица Амо Сагияна, Ереван',0,'https://list.am/user/365508',NULL,1,3,1,0,'Есть',1,0,84,1,'2 недели','Евроремонт','Дом','Каменное',NULL,1,'Арабкир',260000);
INSERT INTO advertisement VALUES(18975012,'https://s.list.am/f/674/68429674.webp','Двухэтажный каменный дом, Erebuni St в Эребуни, 250 кв.м., дизайнерский ремонт',690,'USD','Сдается в аренду квартира В квартире есть все коммунальные услуги удобства: * Система отопления * Газовая плита * Телевизор * Холодильник * Автоматическая стиральная машина * Долгосрочная аренда депозит за 1 месяц: Վարձով է տրվում 3 սենյականոց տուն իր բոլոր հարմարություններով՝3 սենյակ, մեկ սանհանգույց, պատշգամբ։ տեսարան դեպի արարատ: Առանց միջնորդ Переведено с армянского','2023-02-07T05:38:04+00:00','2024-04-30T21:32:00','Erebuni St, Yerevan',1,'https://list.am/user/1979215',NULL,0,3,1,0,'Есть',1,NULL,250,100,'1 месяц','Дизайнерский ремонт','Дом','Каменное','Телевизор, камин, шашлычная печь',2,'Эребуни',274620);
INSERT INTO advertisement VALUES(19292182,'https://s.list.am/f/478/76978478.webp','Двухэтажный каменный дом, 5-й переулок Вштуни в Ачапнякe, 80 кв.м., евроремонт',260000,'AMD','Возможна аренда с оборудованием на срок от 6 месяцев и более (подробные фото по телефону) Переведено с армянского','2023-04-11T10:02:05+00:00','2024-04-30T23:15:00','Վշտունու 5-րդ նրբանցք 25, Երևան',0,'https://list.am/user/2648535','Холодильник, плита, стиральная машина, водонагреватель',1,3,1,0,'Есть',1,0,80,65,'1 месяц','Евроремонт','Дом','Каменное','Телевизор, интернет, кондиционер, охрана',2,'Ачапняк',260000);
INSERT INTO advertisement VALUES(19726774,'https://s.list.am/f/245/80029245.webp','Одноэтажный каменный дом на ул. Карапета Улнеци в Зейтун Канакерe, 80 кв.м., евроремонт',250000,'AMD','Сдается 2 эт отдельный дом, с гаражом в Канакере Состоит из зала с кухней и 2- х спален. Тихое спокойное место. Машину можно также ставить перед домом.Есть небольшой сад с фруктовыми деревьями, с мангалом. Дом находится в районе с развитой инфраструктурой, все рядом.Имеется отопление бакси и интернет. В доме могут жить 4-6 человек. Звоните за подробностями.','2023-07-14T09:01:03+00:00','2024-04-30T23:50:00','Улица Карапета Улнеци, Yerevan',1,'https://list.am/user/68949','Холодильник, плита, стиральная машина, водонагреватель, утюг, фен',1,3,1,0,'Есть',1,0,80,80,'1 месяц','Евроремонт','Дом','Каменное','Телевизор, интернет',1,'Зейтун Канакер',250000);
INSERT INTO advertisement VALUES(20694075,'https://s.list.am/f/765/78416765.webp','Одноэтажный каменный дом на ул. Герцена в Зейтун Канакерe, 150 кв.м., 2 ванные, капитальный ремонт',1100,'USD','Վարձով է տրվում երկհարկանի առանձնատան երկրորդ հարկը` Ամբողջությամբ առանձին: Առանձնատունը նորակառույց է, կապիտալ վերանորոգված: Ամբողջությամբ կահավորված է, հագեցած անհրաժեշտ տեխնիկայով, բոլոր կոմունալ հարմարություններով, առկա է UCOM ինտերնետ կապ և հեռուստատեսություն, կոնդիցիոներ: Առանձնատունն ունի 4 ննջարան, 2 սանհանգույց, խոհանոց, հյուրասենյակ, բաց պատշգամբ, բակում առկա է տաղավար` 20 հոգու համար նախատեսված, մանղալ, ավտոմեքենայի համար նախատեսված կայանատեղի: Առանձնատունը նախատեսված է մինչև 10 հոգու համար: Տրվում է վարձակալության հետևյալ ժամկետներով` Մինչեւ 3 օրը ըստ պայմանավորվածության: 3 -10 օր – օրը 80 ԱՄՆ դոլարին համարժեք դրամ Երկարաժամկետ - 1100 ԱՄՆ դոլարին համարժեք դրամ Գինը սակարկելի: Сдается второй этаж двухэтажного частного дома, полностью раздельный. Дом новой постройки, полностью отремонтирован. Полностью меблирована, оснащена необходимой техникой, всеми коммуникациями, UCOM интернетом и ТВ, кондиционером. В доме 4 спальни, 2 санузла, кухня, гостиная, открытый балкон, беседка на 20 человек, мангал, парковочное место для автомобиля. Дом рассчитан на проживание до 10 человек. Сдается в аренду на следующих условиях. До 3-х дней по договоренности 3 -10 дней - драм эквивалентен 80 долларов США в день Долгосрочный - драм эквивалентен 1100 долларов США в месяц Цена договорная. The second floor of a two-story private house is for rent, completely separate. The house is newly built, fully renovated. It is fully furnished, equipped with necessary equipment, all utilities, UCOM Internet connection and TV, air conditioning. The house has 4 bedrooms, 2 bathrooms, kitchen, living room, open balcony, in the yard there is a pavilion for 20 people, a barbecue, and a parking space for a car. The house is designed for up to 10 people. It is rented for the following terms. Up to 3 days by arrangement 3-10 days - AMD equivalent to 80 USD per day Long-term - AMD equivalent to 1100 USD per month. Price negotiable.','2024-02-25T05:15:01+00:00','2024-04-30T21:56:00','Улица Герцена, Ереван',0,'https://list.am/user/102381','Холодильник, плита, микроволновка, кофеварка, посудомоечная машина, стиральная машина, сушильная машина, водонагреватель, утюг, фен',1,5,2,0,'Есть',1,NULL,150,500,'По договоренности','Капитальный ремонт','Дом','Каменное','Телевизор, интернет, кондиционер, шашлычная печь, беседка, охрана',1,'Зейтун Канакер',437800);
INSERT INTO advertisement VALUES(20798445,'https://s.list.am/f/529/79018529.webp','Двухэтажный дом на пр. Азатутяна в Зейтун Канакерe, 120 кв.м., капитальный ремонт',450000,'AMD','Здаётся в аренду частный дом. С общей площадью 310 кв/м. Для получение дополнительных информации звоните.','2024-03-20T18:47:02+00:00','2024-04-30T21:35:00','Проспект Азатутяна, Ереван',1,'https://list.am/user/1937584','Холодильник, плита, микроволновка, кофеварка, стиральная машина, сушильная машина',1,3,1,0,'Есть',1,1,120,310,'1 месяц','Капитальный ремонт','Дом','Монолит','Телевизор, интернет, кондиционер, камин, шашлычная печь',2,'Зейтун Канакер',450000);
INSERT INTO advertisement VALUES(20915710,'https://s.list.am/f/521/79718521.webp','Двухэтажный каменный дом в Эребуни, 90 кв.м.',130000,'AMD','Сдается частный дом в районе Сари с отдельным входом с просторным двором с коммуналкой Переведено с армянского','2024-04-18T05:45:03+00:00','2024-04-30T22:52:00','Ереван › Эребуни',0,'https://list.am/user/2997605','Холодильник, плита, стиральная машина, водонагреватель',1,3,1,0,'Есть',1,0,90,20,'2 месяца','Старый ремонт','Дом','Каменное',NULL,2,'Эребуни',130000);
INSERT INTO advertisement VALUES(20936907,'https://s.list.am/f/828/79852828.webp','Двухэтажный каменный дом на ул. Андраника Зоравара в Малатия Себастии, 80 кв.м., капитальный ремонт',200000,'AMD','Дом расположен в районе ХАТ б3 возле дома Андраника 109: Недавно отремонтированный и нежилой. Переведено с армянского','2024-04-23T16:27:01+00:00','2024-04-30T23:11:00','Улица Андраника Зоравара 109, Ереван',0,'https://list.am/user/1932194',NULL,0,3,1,0,'По договоренности',1,1,80,80,'1 месяц','Капитальный ремонт','Дом','Каменное',NULL,2,'Малатия Себастия',200000);
INSERT INTO advertisement VALUES(20950992,'https://s.list.am/f/152/79944152.webp','Одноэтажный каменный дом на ул. Себастия в Малатия Себастии, 80 кв.м., косметический ремонт',200000,'AMD','Свой дом, во дворе, со всеми удобствами. Переведено с армянского','2024-04-27T09:24:03+00:00','2024-04-30T22:50:00','Улица Себастия 126, Ереван',0,'https://list.am/user/3004951','Холодильник, плита, микроволновка, стиральная машина, водонагреватель',0,3,1,0,'Есть',1,NULL,80,40,'По договоренности','Косметический ремонт','Дом','Каменное','Телевизор, интернет, кондиционер',1,'Малатия Себастия',200000);
INSERT INTO advertisement VALUES(20951827,'https://s.list.am/f/606/79949606.webp','Одноэтажный каменный дом, Ծխախոտագործների փողոց в центре, 95 кв.м., частичный ремонт',250000,'AMD','В квартире 2 этажа, 2 этаж сдается, 2 спальни, 2 коридора, 1 балкон, просторная гостиная и кухня. Квартира сдается на срок не менее 6 месяцев и с обязательным залогом Переведено с армянского','2024-04-27T12:46:06+00:00','2024-04-30T22:16:00','Ծխախոտագործների փողոց, Երևան',0,'https://list.am/user/3005340','Холодильник, стиральная машина, водонагреватель',0,3,1,0,'Есть',NULL,0,95,1,'1 месяц','Частичный ремонт','Дом','Каменное','Телевизор, интернет',1,'Кентрон',250000);
CREATE TABLE telegram_user_filtres (
        user_id INTEGER PRIMARY KEY,
        chat_id INTEGER NOT NULL,
        send_duplicates BOOLEAN DEFAULT 1,
        price_value_amd INTEGER DEFAULT NULL,
        agent_status BOOLEAN DEFAULT NULL,
        garage BOOLEAN DEFAULT NULL,
        rooms_count INTEGER DEFAULT NULL,
        toilet_count INTEGER DEFAULT NULL,
        furniture TEXT DEFAULT NULL,
        children_allowed BOOLEAN DEFAULT NULL,
        animals_allowed BOOLEAN DEFAULT NULL,
        total_area INTEGER DEFAULT NULL,
        land_area INTEGER DEFAULT NULL,
        floors_count INTEGER DEFAULT NULL,
        district VARCHAR(50) DEFAULT NULL
);
INSERT INTO telegram_user_filtres VALUES(12345678,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO telegram_user_filtres VALUES(87654321,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
CREATE TABLE sent_adv (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        adv_id INTEGER NOT NULL,
        tlg_user_id TEXT NOT NULL,
        FOREIGN KEY(adv_id) REFERENCES advertisement(id),
        FOREIGN KEY(tlg_user_id) REFERENCES telegram_user(user_id)

);
COMMIT;
