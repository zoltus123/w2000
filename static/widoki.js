/**
 * Created by miki on 13.05.17.
 */
function widokWynikow() {
    $('#komunikaty').empty();
    $('#dane').empty().append(
        "<header>Statystyki: </header>" +
        "<section id='mapa_dane'><div id='mapa_div'></div><div id='dane_div'>" +
        "<div id='statystyki_div'><header><h4>Zbiorcze statystyki głosowania:</h4></header>" +
        "<table id='statystyki_tabelka'></table></div><div id='frekwencja_div'></div></div></section>"
    );
    $('#wyniki').empty().append(
        "<header>Wyniki wyborów:</header>" +
        "<table id='wyniki_tabelka'><tr><td>Lp</td><td>Imię i nazwisko</td><td>Liczba oddanych głosów</td>" +
        "<td class='wyniki_procenty'>Wynik wyborczy (%)</td></tr>"
    );
    $('#linki').empty()
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


function widokObwodu(obw_id) {
    widokWynikow();

    $.getJSON("/rest/obwod/" + obw_id, function ( data ) {
        nawigujObw(data.obwod, data.gmina, data.powiat, data.wojewodztwo);
        wypelnijStatystyki(data.statystyki, data.wyniki);
        wypelnijFrekwencje(data.frekwencja);
        wypelnijWyniki(data.kandydaci, data.wyniki, data.pozycje, data.procenty);
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
        wypelnijStatystyki(data.statystyki, data.wyniki);
        wypelnijFrekwencje(data.frekwencja);
        wypelnijWyniki(data.kandydaci, data.wyniki, data.pozycje, data.procenty);
        wypelnijWojewodztwa(data.wojewodztwa);
        google.charts.setOnLoadCallback(function() {
            narysujMape(data.wojewodztwa, data.frekwencjaWoj);
        });

    });
}