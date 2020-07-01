CREATE  TABLE  temp_clientes_tme AS (SELECT DISTINCT identificacion FROM plano_operaciones_me ) ;
SELECT COUNT(*) FROM temp_clientes_tme WHERE identificacion NOT IN ( SELECT identificacion FROM consdavivienda_cliente) ;

CREATE  TABLE temp_clientes_tme_nocl AS  (
SELECT p.identificacion FROM  temp_clientes_tme as   p 
LEFT JOIN consdavivienda_cliente as cl 
ON  p.identificacion = cl.identificacion 
WHERE cl.identificacion IS NULL 
);


CREATE TABLE temp_resu_fech_tme AS ( 
SELECT fecha::date,identificacion,SUM(monto_usd) as monto_usd FROM plano_operaciones_me GROUP BY  1,2 );


CREATE TABLE temp_total_monto_tme AS ( 
SELECT identificacion,SUM(monto_usd) as total_monto_usd FROM plano_operaciones_me GROUP BY  1 );

CREATE TABLE temp_resu_tm_trimestre1 AS (
SELECT identificacion,SUM(monto_usd) as total_trimestre  FROM  temp_resu_fech_tme WHERE fecha >='2018-10-01' AND fecha<='2018-12-31'  GROUP BY 1 );

CREATE TABLE temp_resu_tm_trimestre2 AS (
SELECT identificacion,SUM(monto_usd) as total_trimestre  FROM  temp_resu_fech_tme WHERE fecha >='2019-01-01' AND fecha< '2019-04-01'  GROUP BY 1 );

CREATE TABLE temp_resu_tm_trimestre3 AS (
SELECT identificacion,SUM(monto_usd) as total_trimestre  FROM  temp_resu_fech_tme WHERE fecha >='2019-04-01' AND fecha< '2019-07-01'  GROUP BY 1 );

CREATE TABLE temp_resu_tm_trimestre4 AS (
SELECT identificacion,SUM(monto_usd) as total_trimestre  FROM  temp_resu_fech_tme WHERE fecha >='2019-07-01' AND fecha< '2019-10-01'  GROUP BY 1 );


CREATE TABLE temp_parc_trime_1 AS  (
SELECT clme.identificacion , tm1.total_trimestre as trimestre1 
FROM temp_clientes_tme clme 
LEFT JOIN temp_resu_tm_trimestre1 tm1 ON tm1.identificacion = clme.identificacion  );

CREATE TABLE temp_parc_trime_2 AS  (
SELECT clme.* , tm1.total_trimestre as trimestre2
FROM temp_parc_trime_1 clme 
LEFT JOIN temp_resu_tm_trimestre2 tm1 ON tm1.identificacion = clme.identificacion  );


CREATE TABLE temp_parc_trime_3 AS  (
SELECT clme.* , tm1.total_trimestre as trimestre3
FROM temp_parc_trime_2 clme 
LEFT JOIN temp_resu_tm_trimestre3 tm1 ON tm1.identificacion = clme.identificacion  );


CREATE TABLE temp_parc_trime_4 AS  (
SELECT clme.* , tm1.total_trimestre as trimestre4
FROM temp_parc_trime_3 clme 
LEFT JOIN temp_resu_tm_trimestre4 tm1 ON tm1.identificacion = clme.identificacion  );

UPDATE temp_parc_trime_4 SET trimestre1 =0 WHERE trimestre1 IS NULL ; 
UPDATE temp_parc_trime_4 SET trimestre2 =0 WHERE trimestre2 IS NULL ;
UPDATE temp_parc_trime_4 SET trimestre3 =0 WHERE trimestre3 IS NULL ;
UPDATE temp_parc_trime_4 SET trimestre4 =0 WHERE trimestre4 IS NULL ;


CREATE TABLE temp_maestra_trimestre_tme AS ( 
SELECT p.identificacion,p.trimestre1 as total_monto ,'1' as n_trimestre FROM  temp_parc_trime_1 as  p
UNION 
SELECT p.identificacion,p.trimestre2 as total_monto,'2' as n_trimestre FROM  temp_parc_trime_2 as  p
UNION
SELECT p.identificacion,p.trimestre3 as total_monto,'3' as n_trimestre FROM  temp_parc_trime_3 as p
UNION
SELECT p.identificacion,p.trimestre4 as total_monto,'4' as n_trimestre FROM  temp_parc_trime_4 as  p
); 

UPDATE temp_maestra_trimestre_tme  SET total_monto=0 WHERE total_monto is NULL ;

CREATE TABLE temp_conteo_ceros AS (
SELECT identificacion ,COUNT(*)  as total_cero FROM temp_maestra_trimestre_tme WHERE total_monto=0 GROUP BY 1
); 

CREATE TABLE temp_parc_trime_5  AS (
SELECT p.*,t.total_cero FROM temp_parc_trime_4 as p 
LEFT JOIN temp_conteo_ceros as t ON p.identificacion = t.identificacion 
) ; 

UPDATE temp_parc_trime_5 SET total_cero=0 WHERE total_cero IS NULL ; 

--calculo desvicion estadar : 
CREATE TABLE temp_desv_prom_trimestre AS ( 
SELECT identificacion,STDDEV(total_monto) as desviacion_trimestre,AVG(total_monto) as promedio  
FROM temp_maestra_trimestre_tme GROUP BY 1 );

CREATE TABLE temp_parc_trime_6  AS (
SELECT p.*,t.desviacion_trimestre,t.promedio FROM temp_parc_trime_5 as p 
LEFT JOIN temp_desv_prom_trimestre as t ON p.identificacion = t.identificacion  
); 

CREATE TABLE temp_parc_trime_7  AS (
SELECT p.*,(t.desviacion_trimestre/t.promedio) as coeficiente FROM temp_parc_trime_6 as p 
LEFT JOIN temp_desv_prom_trimestre as t ON p.identificacion = t.identificacion  
);

--- Calculos maximos y minimo de toda la ventana de tiempo : 
CREATE TABLE temp_maximo_minimos_motos as (
SELECT identificacion,MAX(monto_usd) as maximo_monto,MIN(monto_usd) as minimo_monto  FROM plano_operaciones_me GROUP BY 1 
);

CREATE TABLE temp_parc_trime_8  AS (
SELECT p.*,t.maximo_monto,t.minimo_monto FROM temp_parc_trime_7 as p 
LEFT JOIN temp_maximo_minimos_motos as t ON p.identificacion = t.identificacion  
);


CREATE TABLE temp_parc_trime_9  AS (
SELECT p.*, (CASE WHEN t.identificacion IS NULL THEN 'SI' ELSE 'NO' END) as escliente  FROM temp_parc_trime_8 as  p
LEFT JOIN  temp_clientes_tme_nocl as t  
ON p.identificacion = t.identificacion 
);

CREATE TABLE temp_parc_trime_10  AS (
SELECT p.*, t.segmento_comercial as  segmento_comercial_pn,t.subsegmento_comercial as  subsegmento_comercial_pn ,t.segmento_color as segmento_color_pn ,t.ciiu_restr as ciiu_restr_pn ,t.lista_restr as lista_restr_pn 
FROM temp_parc_trime_9 as  p
LEFT JOIN  consdavivienda_resumeninfopersonanatural as t  
ON p.identificacion = t.identificacion 
);

CREATE TABLE temp_parc_trime_11  AS (
SELECT p.*, t.segmento_comercial as  segmento_comercial_pj,t.subsegmento_comercial as  subsegmento_comercial_pj ,t.segmento_color as segmento_color_pj ,t.ciiu_restr as ciiu_restr_pj ,t.lista_restr as lista_restr_pj 
FROM temp_parc_trime_10 as  p
LEFT JOIN  consdavivienda_resumeninfopersonajuridica as t  
ON p.identificacion = t.identificacion 
);

CREATE TABLE temp_coef_tiempo  AS (
SELECT identificacion,antiguedad,(antiguedad::double precision/360) coef_tiemp  FROM consdavivienda_resumeninfopersonanatural
) ;

CREATE TABLE temp_parc_trime_12  AS (
SELECT p.*, t.coef_tiemp
FROM temp_parc_trime_11 as  p
LEFT JOIN  temp_coef_tiempo as t  
ON p.identificacion = t.identificacion 
);

CREATE TABLE temp_parc_trime_13  AS (
SELECT p.*,0::double precision as cupo 
FROM temp_parc_trime_12 as  p
);

CREATE TABLE temp_prom_trimestre  AS (
SELECT identificacion,MIN(total_monto) as minimo_trimestre ,MAX(total_monto) as maximo_trimestre ,AVG(total_monto) as promedio_trimestre 
FROM  temp_maestra_trimestre_tme 
GROUP BY 1
) ;


CREATE TABLE temp_parc_trime_14  AS (
SELECT p.*, t.minimo_trimestre,t.maximo_trimestre,t.promedio_trimestre
FROM temp_parc_trime_13 as  p
LEFT JOIN  temp_prom_trimestre as t  
ON p.identificacion = t.identificacion 
);


CREATE TABLE temp_parc_trime_15  AS (
SELECT p.*,  (CASE WHEN t.identificacion  IS NULL THEN 'NO' ELSE 'SI'  END) as es_persona_natural
FROM temp_parc_trime_14 as  p
LEFT JOIN  consdavivienda_resumeninfopersonanatural as t  
ON p.identificacion = t.identificacion 
);


CREATE TABLE temp_parc_trime_16  AS (
SELECT p.*,  (CASE WHEN t.identificacion  IS NULL THEN 'NO' ELSE 'SI'  END) as es_persona_juridica
FROM temp_parc_trime_15 as  p
LEFT JOIN  consdavivienda_resumeninfopersonajuridica as t  
ON p.identificacion = t.identificacion 
);

CREATE TABLE temp_parc_trime_17  AS (
SELECT p.*,  t.total_monto_usd
FROM temp_parc_trime_16 as  p
LEFT JOIN  temp_total_monto_tme as t  
ON p.identificacion = t.identificacion 
);



--- Reglas  : 
--SELECT identificacion,(maximo_trimestre*4) as valor FROM  temp_parc_trime_14  WHERE coeficiente >=0 and coeficiente<= 0.5 LIMIT 10;
-- regla 1 
UPDATE temp_parc_trime_17 SET cupo = (maximo_trimestre*4)  WHERE coeficiente >=0 and coeficiente<= 0.5 ;
-- regla 2 
SELECT identificacion,(promedio_trimestre*4) as valor FROM  temp_parc_trime_17  WHERE coeficiente > 0.5 and coeficiente<= 1 ;
UPDATE temp_parc_trime_17 SET cupo = (promedio_trimestre*4)  WHERE coeficiente > 0.5 and coeficiente<= 1 ;
-- regla 3 
SELECT identificacion,(promedio_trimestre*4) as valor FROM  temp_parc_trime_17  WHERE coeficiente > 1 and coeficiente<= 1.5 ;
UPDATE temp_parc_trime_17 SET cupo = (trimestre1+trimestre2+trimestre3+trimestre4)  WHERE coeficiente > 1 and coeficiente<= 1.5 ;
-- regla 4 
SELECT identificacion,(maximo_trimestre *2) as valor FROM  temp_parc_trime_17  WHERE coeficiente > 1.5 and coeficiente<= 1.8 ;
UPDATE temp_parc_trime_17 SET cupo = maximo_trimestre *2   WHERE coeficiente > 1.5 and coeficiente<= 1.8 ;
--regla 5 : 
SELECT identificacion,(promedio_trimestre*4) as valor FROM  temp_parc_trime_17  WHERE coeficiente > 1.8 and coeficiente<= 2.1 ;
UPDATE temp_parc_trime_17 SET cupo = promedio*6  WHERE coeficiente > 1.8 and coeficiente<= 2.1 ;

-- regla 6 
SELECT  COUNT(*) FROM temp_parc_trime_17  WHERE ciiu_restr_pn NOT IN ('OK','NA')  ;
UPDATE temp_parc_trime_17 SET cupo = 0  WHERE ciiu_restr_pn NOT IN ('OK','NA')  ;

--- Regla 7 
SELECT  COUNT(*) FROM temp_parc_trime_17  WHERE lista_restr_pn ='S'  ;
UPDATE temp_parc_trime_17 SET cupo = 0  WHERE lista_restr_pn ='S';


SELECT COUNT(*) FROM  temp_parc_trime_17  WHERE (ciiu_restr_pn !='OK' OR ciiu_restr_pj !='OK');

COPY temp_parc_trime_17 TO 'C:\Users\fruiz\OneDrive - Asesoftware S.A.S\BKASW\Documentos\sql\PLANO_CUPOS_27021020.csv' ENCODING 'UTF8' DELIMITER ';' CSV HEADER;





--DROP TABLE temp_parc_trime_1;
--DROP TABLE temp_parc_trime_2;
--DROP TABLE temp_parc_trime_3;
--DROP TABLE temp_parc_trime_4;

SELECT identificacion,SUM(monto_usd) as total_trimestre  FROM  temp_resu_fech_tme WHERE fecha >='2019-07-01' AND fecha< '2019-10-01'  AND identificacion ='41372224' GROUP BY 1


