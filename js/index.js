/* # index.js is part of Barleymap web app.
 * # Copyright (C)  2013-2014  Carlos P Cantalapiedra.
 * # (terms of use can be found within the distributed LICENSE file).
*/
$(document).ready(function(){
    
    // Preload from current values
    //
    if($('#show_genes').is(':checked') || $('#show_markers').is(':checked') || $('#show_anchored').is(':checked')) {
        $("#onmarker_fieldset").show();
        
        //if($('#on_intervals').is(':checked')) {
        $("#extend_fieldset").show();
            //$("#genes_text").text("Additional information will be added to the results.");
        //}
    } else {
        //$("#genes_text").text("");
        $("#onmarker_fieldset").hide();
        $("#extend_fieldset").hide();
    }
    
    if($("#extend").is(':checked')){
        $("#extend_text").show();
        if ($("#sort_cm").is(":checked")) {
                $("#extend_cm").show();
                $("#extend_bp").hide();
            } else {
                $("#extend_cm").hide();
                $("#extend_bp").show();
            }
    } else {
        $("#extend_text").hide();
        $("#extend_cm").hide();
        $("#extend_bp").hide();
    }
    
    if ($('#aligner').children(":selected").val() == "gmap,blastn") {
        $("#algorithm_text").text("Perform a GMAP search, followed by BLASTN alignment for unmapped sequences.");
    } else if ($('#aligner').children(":selected").val() == "gmap") {
        $("#algorithm_text").text("Perform a GMAP alignment.");
    } else if ($('#aligner').children(":selected").val() == "blastn") {
        $("#algorithm_text").text("Perform a BLASTN search.");
    }
    
    // Events
    //
    // LOAD DEMO SEQUENCES
    $("#align_demo_button").click(function(){
        $("#align_query").text(">SCRI_RS_129789\n\
AATTTACTGGTACTATGCGCAAMTATTGAAGGYCGATGAGGAAGAGTTTGGAGGCCACGGNGCGCTGCTTCAGGAGGGGATGTTCGCGTCTTTCACCCTTTTCCTGCTTTCATGGATTCTT\n\
>12_30948\n\
GTAGCAATCCGCCCGTGCAGGTTCCAATGGCGAGCTCGACTTGTTCCGATGACAAGGTTGNTCCCCTGGTTCAGAAACACGCACCCGCCGGAAWCCCGGAGGCGCTTACGACGACGAAGAA\n\
>SCRI_RS_130600\n\
CGATGAAGAAGGAGCGATCGAGAAACTCCTCCGGTGGTCCGCCGCGACATTGGAGGCAACNGCCTTGTGGGTTGCTGCTATATGTGGGGGCAAGGACCGTGATGTCTAAGTGTGCCCTGAA\n\
>SCRI_RS_189465\n\
ATAGAGCAATATTACTTGCATTCAGTTTTGTGTCGTCGTGGAAATTCAGATGGCCGTCTCNTGACGCCACAACGTCTTCATTCAGATCTTAATTGGAAAGCAAGAACCAAATTCTTTTTTT\n"
        );
    });
    
    $("#clear_demo_button").click(function(){
        $("#align_query").text("");
        $("#find_query").text("");
        $("#locate_query").text("");
    });
    
    // LOAD DEMO IDS
    $("#find_demo_button_full").click(function(){
        $("#find_query").text("11_10419\n11_20854\n11_20855\n11_20856\n\
SCRI_RS_104699\n11_20851\nSCRI_RS_66562\n12_11139\nSCRI_RS_104697\nSCRI_RS_135425\nBK_19\n11_11127\n\
12_11504\nSCRI_RS_144535\nSCRI_RS_175682\nBK_10\nBK_10\nBK_10\nBK_10\nBK_10\nBK_11\n\
BK_12\nBK_13\nBK_14\nBK_16\nBK_17\nSCRI_RS_10111\nSCRI_RS_169728\n11_20320\n11_10933\n\
11_20454\n11_10935\n11_20325\n11_20458\n11_10939\n11_20328\n11_20853\nSCRI_RS_228070\n\
SCRI_RS_177919\nSCRI_RS_159526\n11_11359\nSCRI_RS_235243\nSCRI_RS_154541\nSCRI_RS_177133\n\
SCRI_RS_182637\nSCRI_RS_4697\n11_11352\n11_11350\n12_11181\n12_11183\n11_11354\nSCRI_RS_197270\n\
11_11222\n11_11221\n11_20537\n11_11227\n11_11224\n11_10336\nSCRI_RS_148722\nSCRI_RS_204144\n\
SCRI_RS_196677\nSCRI_RS_192360\n11_10331\nSCRI_RS_205658\nSCRI_RS_151894\nSCRI_RS_222357\nSCRI_RS_175469\n\
SCRI_RS_171144\nSCRI_RS_204353\nSCRI_RS_171142\nSCRI_RS_173807\nSCRI_RS_13262\n12_11437\nSCRI_RS_176086\n\
SCRI_RS_140931\nSCRI_RS_176084\n12_10151\n11_21037\nSCRI_RS_157816\nSCRI_RS_222936\n12_11438\n\
SCRI_RS_189167\n12_10923\n11_20524\nSCRI_RS_178618\n11_20526\n11_10807\n11_20521\nSCRI_RS_168603\n\
SCRI_RS_114741\nSCRI_RS_171543\n11_11534\n11_20514\n11_20528\n11_20529\n11_11530\n11_10480\n\
SCRI_RS_1426\nSCRI_RS_198888\nSCRI_RS_128254\nSCRI_RS_223224\nSCRI_RS_1429\n11_10775\n11_20660\n");
    });
    
    //>100002678|F|0 \n\GBS PAVs \n\>100021533|F|0--60:C>G \n\GBS SNPs"
    
    // LOAD DEMO IDS
    $("#find_demo_button_region").click(function(){
        $("#find_query").text("1827-958\n\
12_30054\n\
bPb-3112_WSU_r\n\
3257651\n\
owbGBS33344\n\
U36_54133\n\
AK356240\n\
SCRI_RS_133674\n\
barke_contig_2139962\n\
bowman_contig_619214\n\
morex_contig_1030797\n\
MRX2BAD319P15T71\n\
MLOC_28858\n\
JHI-Hv50k-2016-383738\n\
HORVU6Hr1G057800\n");
    });
    
    // LOAD DEMO POSITIONS
    $("#locate_demo_button").click(function(){
        $("#locate_query").text("chr1H	3770174\n\
chr1H	81042669\n\
chr2H	711398163\n\
chr6H	376635036\n\
chr7H	4184387\n\
chr7H	227367117\n\
morex_contig_1761774	1\n\
morex_contig_1574272	1\n\
morex_contig_1574864	1\n\
morex_contig_1577643	1\n\
bowman_contig_866000	1\n\
bowman_contig_229328	1");
    });
    
    $("#show_genes").change(function(){
        if($('#show_genes').is(':checked') || $('#show_markers').is(':checked') || $('#show_anchored').is(':checked')) {
            $("#onmarker_fieldset").show();
            //if($('#on_intervals').is(':checked')) {
            $("#extend_fieldset").show();
                //$("#genes_text").text("Genes between each two markers will be added to the results.");
            //}
        } else {
            $("#extend_fieldset").hide();
            //$("#genes_text").text("");
            $("#onmarker_fieldset").hide();
        }
    });
    
    $("#show_markers").change(function(){
        if($('#show_genes').is(':checked') || $('#show_markers').is(':checked') || $('#show_anchored').is(':checked')) {
            $("#onmarker_fieldset").show();
            //if($('#on_intervals').is(':checked')) {
            $("#extend_fieldset").show();
                //$("#genes_text").text("Genes between each two markers will be added to the results.");
            //}
        } else {
            $("#extend_fieldset").hide();
            //$("#genes_text").text("");
            $("#onmarker_fieldset").hide();
        }
    });
    
    $("#show_anchored").change(function(){
        if($('#show_genes').is(':checked') || $('#show_markers').is(':checked') || $('#show_anchored').is(':checked')) {
            $("#onmarker_fieldset").show();
            //if($('#on_intervals').is(':checked')) {
            $("#extend_fieldset").show();
                //$("#genes_text").text("Genes between each two markers will be added to the results.");
            //}
        } else {
            $("#extend_fieldset").hide();
            //$("#genes_text").text("");
            $("#onmarker_fieldset").hide();
        }
    });
    
    //$("#on_intervals").change(function(){
    //    $("#extend_fieldset").show();
    //});
    //
    //$("#on_markers").change(function(){
    //    $("#extend_fieldset").hide();
    //});
    
    $("#extend").change(function(){
        if ($(this).is(":checked")) {
            $("#extend_text").show();
            if ($("#sort_cm").is(":checked")) {
                $("#extend_cm").show();
                $("#extend_bp").hide();
            } else {
                $("#extend_cm").hide();
                $("#extend_bp").show();
            }
        } else {
            $("#extend_text").hide();
            $("#extend_cm").hide();
            $("#extend_bp").hide();
        }
    });
    
    $("#sort_cm").click(function(){
        if($("#extend").is(':checked')){
            $("#extend_cm").show();
            $("#extend_bp").hide();
        }
    });
        
    $("#sort_bp").click(function(){
        if($("#extend").is(':checked')){
            $("#extend_cm").hide();
            $("#extend_bp").show();
        }
    });
    
    $("#email_text").hide();
    
    $("#input_send_email").change(function(){
        if ($(this).is(":checked") == "1") {
            $("#email_text").show();
        } else {
            $("#email_text").hide();
        }
        
    });
    
    $("#user_file").change(function(){
        $("#clear_file_button").show();
    });
    
    $("#clear_file_button").click(function(){
        $(this).hide();
        $("#user_file").replaceWith( control = $("#user_file").clone( true ) );
    });
    
    // CHANGE OF ALGORITHM
    $('#aligner').change(function() {
        if ($('#aligner').children(":selected").val() == "gmap,blastn") {
            $("#algorithm_text").text("Perform a GMAP search, followed by BLASTN alignment for unmapped sequences.");
        } else if ($('#aligner').children(":selected").val() == "gmap") {
            $("#algorithm_text").text("Perform a GMAP alignment.");
        } else if ($('#aligner').children(":selected").val() == "blastn") {
            $("#algorithm_text").text("Perform a BLASTN search.");
        }
    });
});