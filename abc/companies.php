<?php

$ua = 210;
        $contador = 0;
        $context = stream_context_create([
            'http' => [
                'header' => "User-Agent: Mozilla/5.1 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.{$ua} Safari/537.36\r\n" . // Cambia MiAgenteDeUsuario por tu propio agente de usuario
                    "Accept-Language: es-ES,es;q=0.9\r\n" // Cambia es-ES,es por los idiomas que prefieras
            ]
        ]);

        $categories = fopen(__DIR__ . "/abc_categories.txt", "r");
        //$subcategoriesDone = fopen(__DIR__ . "/vu_categoriesDone.txt", "a");
        if ($categories) {
            //Bucle que itera por las diferentes categorias
            while (($category = fgets($categories)) !== false) {
                $category = str_replace(array("\r", "\n"), '', $category);
                $page = 1;
                $results = true;
                while ($results) {

                    $line = "https://www.abctelefonos.com$category/espana/pag_$page";
                    echo $category . "->  Página -> " . $page . PHP_EOL;

                    sleep(mt_rand(8, 16));
                    try {
                        $html = new Crawler((file_get_contents($line, false, $context))); //cargar htlm y cambiar cabecera
                    } catch (\Exception $e) {
                        echo 'Error: ' . $e->getMessage();
                        $results = false;
                        continue;
                    }

                    //TODO rehacer si procede
                    //if ($this->companiesServicePag->checkRobots($html)) {
                    //    die("nos han detectado como bots");
                    //}

                    if (!$this->companiesServiceABC->checkNext($html)) {
                        echo "pagina vacia" . PHP_EOL;
                        $results = false;
                    }
                    $contador++;
                    if ($contador > 5) {
                        $ua = $ua + 10;
                        $contador = 0;
                    }

                    if ($divs = $html->filter('div.resultItem')) {
                        foreach ($divs as $div) {
                            $this->companiesServiceABC->extractData($div);
                        }
                        echo("INSERCION DEL BLOQUE " . $line . PHP_EOL);
                        $this->companiesService->callFlush();
                    }
                    sleep(mt_rand(8, 16));
                    $page++;
                    echo("Next page: " . $page . PHP_EOL);
                }
                //die("FIN DE LA CATEGORÍA");
            }
            //fwrite($subcategoriesDone, $subcategory . PHP_EOL);
        }
        //fclose($subcategoriesDone);
        return Command::SUCCESS;