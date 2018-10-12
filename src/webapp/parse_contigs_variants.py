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
from output import print_variants_contigs
from CSVWriter import CSVWriter

contigs_list = []
variants_list = []
vcf_header = ""
samples_filename = ""
output_format = "tabular"
het_to_miss = True
show_monomorph = True
show_effects = True
biallelic = "mono"
numeric = True
cluster_samples = True

def parse_contigs(query, sets_list, start, end, 
                  max_missing, max_heteros, maf,
                  tmp_files_path):
    variants_dict = {}
    
    if query == "" or query == None:
        raise Exception("Query is empty.")
    
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
    query_list = [query]
    
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
    else:
        samples_translation = ""
    
    sys.stderr.write("Processing samples translation list...\n")
    samples_trans_dict = parse_samples_translation(samples_translation) # from util.py
    
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
            if not header_found:
                if line.startswith("#") and vcf_header == "":
                    parse_header(line_data, genotypes_dict, names_dict, \
                                 samples_filename, samples_list, samples_translation, samples_trans_dict)
                    # parse_header from vcf_util.py
                    header_found = True
                    continue
            
            if not header_found:
                raise Exception("No header found nor provided for VCF data.")
            
            total_records += 1
            
            contig = line_data[VCF_CONTIG_COL]
            if not contig in query_list: continue
            #sys.stderr.write(contig+"\n")
            
            pos = long(line_data[VCF_POS_COL])
            if (start != 0 and pos < start): continue
            if (end != 0 and pos > end): break
            if len(variants_list) > 0 and not [contig, pos] in variants_list: continue
            #sys.stderr.write(str(pos)+"\n")
            #sys.stderr.write(str(start)+"\n")
            #sys.stderr.write(str(end)+"\n")
            
            total_variants+=1
            var_id = total_variants
            
            variant_dict = {'var_id':var_id, 'contig':contig, 'pos':pos, \
                            'ref':line_data[VCF_REF_COL], 'alt':line_data[VCF_ALT_COL], \
                            'alleles':{}, 'effs':{}, 'eff_x':[]}
            
            if show_effects: load_effects(line_data, variant_dict)
            
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
    print_variants_contigs(variants_dict, genotypes_dict, names_dict, samples_list, \
                           show_effects, output_format, \
                           biallelic, numeric, cluster_samples, csv_fileo)
    
    csv_fileo.close()
    
    sys.stderr.write("Total records read: "+str(total_records)+"\n")
    sys.stderr.write("Total variants parsed: "+str(total_variants)+"\n")
    sys.stderr.write("Total variants output: "+str(total_output)+"\n")
    sys.stderr.write("Finished.\n")
    
    return csv_file

## END
