/**
 * Created by miki on 13.05.17.
 */
function pokazFormularzLogowania() {
    $('#formularz_logowania').show();
}

function ukryjFormularzLogowania() {
    $('#formularz_logowania').hide();
}

function zaloguj() {
    var username = $('#username').val();
    if(!username || username.length === 0) {
        return alert("Podaj login!");
    }
    var password = $('#password').val();
    if(!password || password.length === 0) {
        return alert("Podaj hasło!");
    }

    $.post("/rest/login/", {'username': username, 'password': password}, function (data) {
        if(data.komunikat === 'zalogowano') {
            localStorage.setItem('username', username);
            localStorage.setItem('password', password);
        }
    });
}

function wyloguj() {
    $.post("/rest/logout/", function (data) {

    });
}

function widokWynikow() {
    wyczyscStrone();
    $('#dane').append(
        "<header>Statystyki: </header>" +
        "<section id='mapa_dane'><div id='dane_div'>" +
        "<div id='statystyki_div'><header><h4>Zbiorcze statystyki głosowania:</h4></header>" +
        "<table id='statystyki_tabelka'></table></div><div id='frekwencja_div'></div></div></section>"
    );
    $('#wyniki').append(
        "<header>Wyniki wyborów:</header>" +
        "<table id='wyniki_tabelka'>"
    );
}


function widokWyszukiwania() {
    wyczyscStrone();
    $('#wyniki').append(
        "<header>Wyniki wyszukiwania: </header><ul id='lista_gmin'></ul>"
    );
}

function widokEdycji(obw_id, kand_id) {
    wyczyscStrone();
    $.getJSON("/rest/edycjaDane?obw_id=" + obw_id + "&kand_id=" + kand_id, function (data) {
        $('#dane').append(
        "<header>Edytuj wynik kandydata:</header>" +
        "<table>" +
            "<tr><td>Kandydat:</td><td>" +  data.kandydat.imie + " " + data.kandydat.nazwisko + "</td></tr>" +
            "<tr><td>Województwo:</td><td><a href='#' onclick='widokWojewodztwa(" + data.wojewodztwo.id + ")'>" +
                data.wojewodztwo.nazwa + "</a></td></tr>" +
            "<tr><td>Powiat:</td><td><a href='#' onclick='widokPowiatu(" + data.powiat.id + ")'>" +
                data.powiat.nazwa + "</a></td></tr>" +
            "<tr><td>Gmina:</td><td><a href='#' onclick='widokGminy(" + data.gmina.id + ")'>" +
                data.gmina.nazwa + "</a></td></tr>" +
            "<tr><td>Obwód nr:</td><td><a href='#' onclick='widokObwodu(" + data.obwod.id + ")'>" +
                data.obwod.numer + "</a></td></tr>" +
            "<tr><td>Wynik:</td><td><form onsubmit='edytujWynik(" + obw_id + ", " + kand_id + ")'>" +
            "<input type='number' id='wynik' min='0' required><input type='submit' value='Zapisz'></form></td></tr>" +
            "</table>"
        );
    });
}

function wyszukajGminy() {
    var wzorzec = $('#pole_wyszukiwarki').val();
    if(wzorzec && wzorzec.length > 2) {
        widokWyszukiwania();
        $.getJSON("/rest/szukaj?wzorzec=" + wzorzec, function (data) {
            $('#wyniki > header').append(data.komunikat);

            for (var gmi in data.gminy) {
                $('#lista_gmin').append(
                    "<li><a href='#' onclick='widokGminy(" + data.gminy[gmi].id + ")'>Gmina " + data.gminy[gmi].nazwa +
                    " (pow. " + data.gminy[gmi].powiat + ")</a></li>"
                );
            }
        });
    }
}


function nawigujPowrot() {
    $('#nav_miejsce').html("<a href='#' onclick='widokKraju()'>Powrót do strony głównej</a>")
}

function wyczyscStrone() {
    nawigujPowrot();
    $('#komunikaty').empty();
    $('#dane').empty();
    $('#wyniki').empty();
    $('#linki').empty();
}

function nawigujKraj() {
    $('#nav_miejsce').html("Jesteś tu: <a href='#' onclick='widokKraju()'>Polska </a>");
}


function nawigujWoj(woj) {
    nawigujKraj();
    $('#nav_miejsce').append("<a href='#' onclick='widokWojewodztwa(" + woj.id + ")'>" + woj.nazwa + " </a>");
}


function nawigujPow(pow, woj) {
    nawigujWoj(woj);
    $('#nav_miejsce').append("<a href='#' onclick='widokPowiatu(" + pow.id + ")'>" + pow.nazwa + " </a>");
}


function nawigujGmi(gmi, pow, woj) {
    nawigujPow(pow, woj);
    $('#nav_miejsce').append("<a href='#' onclick='widokGminy(" + gmi.id + ")'>" + gmi.nazwa + " </a>");
}


function nawigujObw(obw, gmi, pow, woj) {
    nawigujGmi(gmi, pow, woj);
    $('#nav_miejsce').append("<a href='#' onclick='widokObwodu(" + obw.id + ")'>Obwód nr " + obw.numer + " </a>");
}


function wypelnijStatystyki(statystyki, wyniki) {
    var statystykiTabelka = $("#statystyki_tabelka");

    statystykiTabelka.empty();

    for (var stat in statystyki) {
            statystykiTabelka.append(
                        "<tr>"
                            +"<td>"
                                + statystyki[stat]
                            + "</td>"
                            + "<td class='statystyki_pole'>"
                                + wyniki[statystyki[stat]]
                            + "</td>"
                        + "</tr>"
            )
        }
}


function wypelnijFrekwencje(frekwencja) {
    var frekwencjaDiv = $("#frekwencja_div");

    frekwencjaDiv.empty();

    frekwencjaDiv.append(
        "<header><h4>Frekwencja:</h4></header>"
        + "<div class='tloprocentow'>"
            + "<div class='poziomFrekwencji' style='width: " + frekwencja + "%'></div>"
            + frekwencja + "%"
        + "</div>"
    )
}


function wypelnijWyniki(kandydaci, wyniki, pozycje, procenty) {
    var wynikiTabelka = $('#wyniki_tabelka');
    wynikiTabelka.empty();
    wynikiTabelka.append(
      "<tr><td>Lp</td><td>Imię i nazwisko</td><td>Liczba oddanych głosów</td>" +
        "<td class='wyniki_procenty'>Wynik wyborczy (%)</td></tr>"
    );
    i = 1;
    for (var kand in kandydaci) {
        wynikiTabelka.append(
            "<tr>"
                + "<td>"
                    + i
                + "</td>"
                + "<td>"
                    + kandydaci[kand].imie
                    + " "
                    + kandydaci[kand].nazwisko
                + "</td>"
                + "<td>"
                    + wyniki[kandydaci[kand].id]
                + "</td>"
                + "<td class='wyniki_procenty'>"
                    + "<div class='tloprocentow'>"
                        + "<div class='" + pozycje[kandydaci[kand].id]
                        + "' style='width: " + procenty[kandydaci[kand].id] + "%'></div>"
                    + "</div>"
                    + procenty[kandydaci[kand].id]
                    + "%"
                + "</td>"
            + "</tr>"
        );
        i++;
    }
}


function wypelnijWynikiObwodu(kandydaci, wyniki, pozycje, procenty, obw_id) {
    var wynikiTabelka = $('#wyniki_tabelka');
    wynikiTabelka.empty();
    wynikiTabelka.append(
      "<tr><td>Lp</td><td>Imię i nazwisko</td><td>Liczba oddanych głosów</td>" +
        "<td class='wyniki_procenty'>Wynik wyborczy (%)</td><td></td></tr>"
    );
    i = 1;
    for (var kand in kandydaci) {
        wynikiTabelka.append(
            "<tr>"
                + "<td>"
                    + i
                + "</td>"
                + "<td>"
                    + kandydaci[kand].imie
                    + " "
                    + kandydaci[kand].nazwisko
                + "</td>"
                + "<td>"
                    + wyniki[kandydaci[kand].id]
                + "</td>"
                + "<td class='wyniki_procenty'>"
                    + "<div class='tloprocentow'>"
                        + "<div class='" + pozycje[kandydaci[kand].id]
                        + "' style='width: " + procenty[kandydaci[kand].id] + "%'></div>"
                    + "</div>"
                    + procenty[kandydaci[kand].id]
                    + "%"
                + "</td>"
                + "<td>"
                    + "<a href='#' onclick='widokEdycji(" + obw_id + ", " + kandydaci[kand].id + ")'>Edytuj</a>"
                + "</td>"
            + "</tr>"
        );
        i++;
    }
}

function widokObwodu(obw_id) {
    widokWynikow();

    $.getJSON("/rest/obwod/" + obw_id, function ( data ) {
        nawigujObw(data.obwod, data.gmina, data.powiat, data.wojewodztwo);
        wypelnijStatystyki(data.statystyki, data.wyniki);
        wypelnijFrekwencje(data.frekwencja);
        wypelnijWynikiObwodu(data.kandydaci, data.wyniki, data.pozycje, data.procenty, obw_id);
        $('#linki').empty();
    });
}


function wypelnijObwody(obwody) {
    var linki = $("#linki");
    linki.empty();
    linki.append(
        "<header>Obwody:</header>"
    );
    linki.append("<table id='tabela_linkow'>");
    for (var obw in obwody) {
        $('#tabela_linkow').append(
            "<tr>" +
                "<td>" +
                    "<a href='#' onclick='widokObwodu(" +obwody[obw].id + ")'> Obwód nr " + obwody[obw].numer +
                    "</a>" +
                "<td>" +
                    "<a href='#' onclick='widokObwodu(" +obwody[obw].id + ")'>" + obwody[obw].adres +
                    "</a>" +
                "</td>" +
            "</tr>"
        )
    }
}


function widokGminy(gmi_id) {
    widokWynikow();

    $.getJSON("/rest/gmina/" + gmi_id, function ( data ) {
        nawigujGmi(data.gmina, data.powiat, data.wojewodztwo);
        wypelnijStatystyki(data.statystyki, data.wyniki);
        wypelnijFrekwencje(data.frekwencja);
        wypelnijWyniki(data.kandydaci, data.wyniki, data.pozycje, data.procenty);
        wypelnijObwody(data.adresyObwodow);
    });
}


function wypelnijGminy(gminy) {
    var linki = $("#linki");
    linki.empty();
    linki.append(
        "<header>Gminy:</header>"
    );
    linki.append("<ul id='lista_linkow'>");
    for (var gmi in gminy) {
        $('#lista_linkow').append(
            "<li>" +
            "<a href='#' onclick='widokGminy(" +gminy[gmi].id + ")'>"  + gminy[gmi].nazwa + "</a>" +
            "</li>"
        )
    }
}


function widokPowiatu(pow_id) {
    widokWynikow();

    $.getJSON("/rest/pow/" + pow_id, function ( data ) {
        nawigujPow(data.powiat, data.wojewodztwo);
        wypelnijStatystyki(data.statystyki, data.wyniki);
        wypelnijFrekwencje(data.frekwencja);
        wypelnijWyniki(data.kandydaci, data.wyniki, data.pozycje, data.procenty);
        wypelnijGminy(data.gminyWPowiecie );
    });
}


function wypelnijPowiaty(powiaty) {
    var linki = $("#linki");
    linki.empty();
    linki.append(
        "<header>Powiaty:</header>"
    );
    linki.append("<ul id='lista_linkow'>");
    for (var pow in powiaty) {
        $('#lista_linkow').append(
            "<li>" +
            "<a href='#' onclick='widokPowiatu(" +powiaty[pow].id + ")'>"  + powiaty[pow].nazwa + "</a>" +
            "</li>"
        )
    }
}


function widokWojewodztwa(woj_id) {
    widokWynikow();

    $.getJSON("/rest/woj/" + woj_id, function ( data ) {
        nawigujWoj(data.wojewodztwo);
        wypelnijStatystyki(data.statystyki, data.wyniki);
        wypelnijFrekwencje(data.frekwencja);
        wypelnijWyniki(data.kandydaci, data.wyniki, data.pozycje, data.procenty);
        wypelnijPowiaty(data.powiatyWWojewodztwie);
    });
}


google.charts.load('current', {'packages':['geochart']});


function narysujMape(wojewodztwa, frekwencjaWoj) {

        var dataArray = [];

        dataArray.push(['Województwo', 'Frekwencja']);

        for(var woj in wojewodztwa) {
            dataArray.push([wojewodztwa[woj].nazwa, frekwencjaWoj[wojewodztwa[woj].id]])
        }

        var data = google.visualization.arrayToDataTable(dataArray);

        var wojIndex = [];

        for(var woj in wojewodztwa) {
            wojIndex.push(wojewodztwa[woj].id)
        }

        var options = {
            region: 'PL',
            resolution: 'provinces',
            backgroundColor: '#ffffff',
            datalessRegionColor: '#ffffff'
        };

        var chart = new google.visualization.GeoChart(document.getElementById('mapa_div'));

        google.visualization.events.addListener(chart, 'select', function() {
            var selectionIdx = chart.getSelection()[0].row;
            widokWojewodztwa(wojIndex[selectionIdx]);
        });

        chart.draw(data, options);
}


function wypelnijWojewodztwa(wojewodztwa) {
    var linki = $("#linki");
    linki.empty();
    linki.append(
        "<header>Województwa:</header>"
    );
    linki.append("<ul id='lista_linkow'>");
    for (var woj in wojewodztwa) {
        $('#lista_linkow').append(
            "<li>" +
            "<a href='#' onclick='widokWojewodztwa(" +wojewodztwa[woj].id + ")'>"  + wojewodztwa[woj].nazwa + "</a>" +
            "</li>"
        )
    }
}


function widokKraju() {
    widokWynikow();
    $.getJSON("/rest/index", function ( data ) {
        nawigujKraj();
        $('#mapa_dane').prepend("<div id='mapa_div'></div>");
        wypelnijStatystyki(data.statystyki, data.wyniki);
        wypelnijFrekwencje(data.frekwencja);
        wypelnijWyniki(data.kandydaci, data.wyniki, data.pozycje, data.procenty);
        wypelnijWojewodztwa(data.wojewodztwa);
        google.charts.setOnLoadCallback(function() {
            narysujMape(data.wojewodztwa, data.frekwencjaWoj);
        });

    });
}