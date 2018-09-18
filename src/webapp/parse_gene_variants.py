#!/usr/bin/env python
# -*- coding: utf-8 -*-

## CPCantalapiedra - EEAD - CSIC - 2016

## TODO:
# Make use of cyvcf https://github.com/arq5x/cyvcf based on https://github.com/jamescasbon/PyVCF
# Tests

import os, sys, traceback
#from optparse import OptionParser
from vcf_util import *
from util import parse_samples_translation
from output import print_variants_genes
from CSVWriter import CSVWriter

GENES = 0
ISOFS = 1
NONE = -1

vcf_header = ""
variants_list = []
samples_filename = ""
samples_translation = ""
contigs_info = ""
genes_info = ""
output_format = "tabular"
het_to_miss = False
show_monomorph = True
biallelic = "mono"
numeric = True
cluster_samples = True

def parse_genes(query, sets_list, start, end, 
                  max_missing, max_heteros, maf,
                  tmp_files_path):
    variants_dict = {}
    
    if query == "" or query == None:
        raise Exception("Query is empty.")
    
    if "." in query:
        query_list = [query]
        query_type = 1 # ISOF
    else:
        query_list = [query]
        query_type = 0 # GENE
    
    if sets_list == None or len(sets_list) == 0:
        raise Exception("Sets list is empty.")
    
    # all the sets in sets_list are from the same set_id and set_name
    # they only differ in the set_path
    set_id = sets_list[0][0]
    set_name = sets_list[0][1]
    
    sys.stderr.write("Set: "+str(set_id)+" - "+str(set_name)+"\n")
    
    vcf_filenames = [x[2] for x in sets_list]
    
    for vcf_filename in vcf_filenames:
        sys.stderr.write("Filename: "+str(vcf_filename)+"\n")
     
    #### Parse queries file
    ####
    # if query_file != "":
    #     sys.stderr.write("Processing queries list...\n")
    #     query_list = parse_queries_file(query_file)
    
    
    #### Variants to show
    ####
    # if variants_file != "":
    #     sys.stderr.write("Processing variants list...\n")
    #     variants_list = parse_queries_file(variants_file, keys=(1,2))
    variants_list = []
    
    #### Parse samples translation
    ####
    samples_translation = ""
    if (set_id=="ibsc2012"):
        samples_translation = "/home/cantalapiedra/SNP_panels/exome_sbcc/IBSC2012_as_ref/samples.translation"
    elif (set_id=="climbar"):
        samples_translation = ""
    else:
        raise Exception("Unknown set id: "+str(set_id))
    
    sys.stderr.write("Processing samples translation list...\n")
    samples_trans_dict = parse_samples_translation(samples_translation)
    
    #### Parse samples list
    ####
    #sys.stderr.write("Parsing samples list...\n")
    #samples_list = parse_samples_list(samples_filename)
    samples_list = []
    
    #### Parse headers file
    ####
    #header_found = parse_vcf_header_file(vcf_header, genotypes_dict, names_dict, \
    #                                     samples_filename, samples_list, samples_translation, samples_trans_dict)
    header_found = False
    
    genotypes_dict = {}
    names_dict = {}
    
    #### Parse VCF file
    ####
    total_records = 0
    total_variants = 0
    total_output = 0
    sys.stderr.write("Parsing VCF file...\n")
    for vcf_filename in vcf_filenames:
        sys.stderr.write("Processing "+vcf_filename+"\n")
        
        vcf_file = open(vcf_filename, 'r')
        for line in vcf_file:
            
            if line.startswith("##"): continue
            
            line_data = line.strip().split()
            
            # If a header is found, and if no header file was specified
            # record names of genotypes
            if header_found:
                if line.startswith("#"): continue
            elif not header_found:
                if line.startswith("#") and vcf_header == "":
                    parse_header(line_data, genotypes_dict, names_dict, \
                                 samples_filename, samples_list, samples_translation, samples_trans_dict)
                    header_found = True
                    continue
            
            if not header_found:
                raise Exception("No header found nor provided for VCF data.")
            
            total_records += 1
            
            contig = line_data[VCF_CONTIG_COL]
            #sys.stderr.write(str(line_data)+"\n")
            pos = long(line_data[VCF_POS_COL])
            if len(variants_list) > 0 and not [contig, pos] in variants_list: continue
            
            variant_dict = {'var_id':-1, 'contig':contig, 'pos':pos, \
                            'ref':line_data[VCF_REF_COL], 'alt':line_data[VCF_ALT_COL], \
                            'alleles':{}, 'effs':{}, 'eff_x':[]}
            
            ok_variant = load_effects_genes(line_data, variant_dict, query_type, query_list)
            
            if not ok_variant: continue
            
            total_variants+=1
            var_id = total_variants
            variant_dict["var_id"] = var_id
            
            alleles = parse_alleles(line_data, genotypes_dict, biallelic)
            
            variant_dict['alleles'] = alleles
            
            ok_variant = preprocess_variant(alleles, max_heteros, max_missing, show_monomorph, maf, \
                                            biallelic, het_to_miss)
            if ok_variant:
                variants_dict[var_id] = variant_dict
                total_output += 1
                for allele in alleles:
                    for j in alleles[allele]:
                        genotypes_dict[j][var_id] = allele
    
    csv_file = CSVWriter().get_csv_file(tmp_files_path)
    
    csv_fileo = os.fdopen(csv_file[0], 'wb')
    
    #### Output
    ####
    sys.stderr.write("Generating output...\n")
    print_variants_genes(variants_dict, genotypes_dict, names_dict, samples_list, \
                         output_format, \
                         biallelic, numeric, cluster_samples, csv_fileo)
    
    csv_fileo.close()
    
    sys.stderr.write("Total records read: "+str(total_records)+"\n")
    sys.stderr.write("Total variants parsed: "+str(total_variants)+"\n")
    sys.stderr.write("Total variants output: "+str(total_output)+"\n")
    sys.stderr.write("Finished.\n")
    
    return csv_file

## END
