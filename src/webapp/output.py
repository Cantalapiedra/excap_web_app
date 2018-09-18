#!/usr/bin/env python
# -*- coding: utf-8 -*-

## CPCantalapiedra - EEAD - CSIC - 2016

import sys
from vcf_util import get_numeric_allele
from util import f_cluster_samples

def _f_get_samples_rows(outputs_list, samples_list, genotypes_dict, names_dict, biallelic):
    samples_rows = []
    
    sys.stderr.write("Preparing data of samples for clustering...\n")
    header_row = []
    header_row = samples_list
    #for sample in samples_list:
    #    header_row.append(sample)
    
    samples_rows.append(header_row)
    
    for output_line in outputs_list:
        var_id = output_line[0]
        var_row = []
        for sample in samples_list:
            genotype = names_dict[sample]
            #for genotype in genotypes_dict:
            #    if genotypes_dict[genotype]["good_name"] == sample:
            genotype_var_allele = get_numeric_allele(genotypes_dict[genotype][var_id], biallelic)
            var_row.append(genotype_var_allele)
        samples_rows.append(var_row)
    
    sys.stderr.write("Ready for clustering.\n")
    
    return samples_rows

#
def _print_rows(outputs_list, samples_list, variants_dict, genotypes_dict, names_dict,
               output_fmt, biallelic, numeric, outfile = sys.stdout):
    # For each variant/gene position to output
    sys.stderr.write("Printing genotypes...\n")
    
    for output_line in outputs_list:
        var_id = output_line[0]
        #isof_id = output_line[1]
        fields = [str(field) for field in output_line[1:]]
        outfile.write(">\t"+"\t".join(fields))
        
        if output_fmt == "summary":
            outfile.write("\n")
            
        elif output_fmt == "detail":
            outfile.write("\n")
            variant_alleles = variants_dict[var_id]['alleles']
            
            for allele in variant_alleles:
                outfile.write(">>\t")
                outfile.write(allele+"\t")
                genotypes_allele = variant_alleles[allele]
                genotypes_allele = [genotypes_dict[int(genotype)]["good_name"] for genotype in genotypes_allele]
                
                genotypes_allele = sorted(genotypes_allele)
                outfile.write("\t".join(genotypes_allele))
                outfile.write("\n")
                
        elif output_fmt == "tabular":
            for sample in samples_list:
                genotype = names_dict[sample]
                #for genotype in genotypes_dict:
                #    if genotypes_dict[genotype]["good_name"] == sample:
                if biallelic == "bi" or not numeric:
                    outfile.write("\t"+genotypes_dict[genotype][var_id])
                else: # biallelic = "mono" and numeric:
                    numeric_allele = get_numeric_allele(genotypes_dict[genotype][var_id], biallelic)
                    outfile.write("\t"+str(numeric_allele))
            outfile.write("\n")
        
        else:
            raise Exception("Unrecognized output format "+output_fmt+".")
    
    return

##
def _get_contigs_header(show_effects):
    header_list = ["#", "contig", "pos"]
    header_list = header_list + ["ref", "alt"]
    
    if show_effects:
        header_list = header_list + ["effect", "isof", "change", "other"]
    
    return header_list

def _get_contigs_variant(show_effects, variant):
    contig = variant["contig"]
    output_list = [variant["var_id"], contig, variant["pos"]]
        
    output_list = output_list + [variant["ref"], variant["alt"]]
    
    eff_type = []
    eff_isof = []
    eff_aa = []
    
    if show_effects:
        if len(variant["effs"]) == 0:
            eff_type = ["-"]
            eff_isof = ["-"]
            eff_aa = ["-"]
        else:
            for eff in sorted(variant["effs"]):
                variant_eff = variant["effs"][eff]
                eff_type.append(eff)
                eff_isof.append("("+",".join(variant_eff["eff_isof"])+")")
                eff_aa.append("("+",".join(variant_eff["eff_aa"])+")")
        
        output_list = output_list + [",".join(eff_type), ",".join(eff_isof), ",".join(eff_aa), ",".join(variant["eff_x"])]
    
    return output_list

def _get_genes_header():
    header_list = ["#", "isof"]
    # if len(genes_info_dict)>0:
    #     header_list = header_list + genes_info_dict["header"]
    
    header_list = header_list + ["effect", "eff_other", "ref", "alt", "change", "contig", "pos"]
    
    # if len(contigs_info_dict)>0:
    #     header_list = header_list + contigs_info_dict["header"]
    
    return header_list

def _get_genes_effect(variant, variant_eff_isof, variant_eff_aa, eff):
    output_list = []
    
    contig = variant["contig"]
    
    output_list = [variant["var_id"], variant_eff_isof]
    
    # if len(genes_info_dict)>0:
    #     if variant_eff_isof in genes_info_dict:
    #         output_list = output_list + genes_info_dict[variant_eff_isof]
    #     else:
    #         output_list = output_list + genes_info_dict["void"]
    
    output_list = output_list + [eff, ",".join(variant["eff_x"]), \
                    variant["ref"], variant["alt"], variant_eff_aa, \
                    contig, variant["pos"]]
    
    # if len(contigs_info_dict)>0:
    #     if contig in contigs_info_dict:
    #         output_list = output_list + contigs_info_dict[contig]
    #     else:
    #         output_list = output_list + contigs_info_dict["void"]
    
    return output_list

def print_variants_contigs(variants_dict, genotypes_dict, names_dict, samples_list, \
                           show_effects = False, output_fmt = "tabular", \
                           biallelic = "mono", numeric = False, cluster_samples = False, outfile = sys.stdout):
    
    # Prepare output lines
    outputs_list = []
    for variant_id in variants_dict:
        variant = variants_dict[variant_id]
        output_list = _get_contigs_variant(show_effects, variant)
        outputs_list.append(output_list)
    
    # Sort the list of variants to output
    # by isoform, contig and position
    outputs_list = sorted(outputs_list, key=lambda x: (x[1], int(x[2])))  
    
    # Header
    header_list = _get_contigs_header(show_effects)
    outfile.write("\t".join(header_list))
    
    if output_fmt == "tabular":
        if cluster_samples and len(outputs_list)>0:
            samples_rows = _f_get_samples_rows(outputs_list, samples_list, genotypes_dict, names_dict, biallelic)
            samples_list = f_cluster_samples(samples_rows, biallelic) # from util.py
        # else: samples_list = samples_list
        for sample in samples_list:
            outfile.write("\t"+sample)
        
    outfile.write("\n") # END of header row
    
    # Rows
    _print_rows(outputs_list, samples_list, variants_dict, genotypes_dict, names_dict,
               output_fmt, biallelic, numeric, outfile)
    
    return

##

def print_variants_genes(variants_dict, genotypes_dict, names_dict, samples_list, \
                         output_fmt = "tabular", \
                         biallelic = "mono", numeric = False, cluster_samples = False, outfile = sys.stdout):
    
    # Prepare output lines
    outputs_list = []
    for variant_id in variants_dict:
        variant = variants_dict[variant_id]
        
        for eff in variant["effs"]:
            variant_effs = variant["effs"][eff]
            for i, variant_eff_isof in enumerate(variant_effs["eff_isof"]):
                variant_eff_aa = variant_effs["eff_aa"][i]
                output_list = _get_genes_effect(variant, variant_eff_isof, variant_eff_aa, eff)
                outputs_list.append(output_list)    
        
    # Sort the list of variants to output
    # by isoform, contig and position
    outputs_list = sorted(outputs_list, key=lambda x: (x[1], x[7], int(x[8])))
    # if genes_info == "":
    #     outputs_list = sorted(outputs_list, key=lambda x: (x[1], x[7], int(x[8])))
    # else:
    #     add_fields = genes_info_dict["fields"]
    #     
    #     outputs_list = sorted(outputs_list, key=lambda x: (x[1], x[7+add_fields], int(x[8+add_fields])))
    
    # Header
    header_list = _get_genes_header()
    outfile.write("\t".join(header_list))
    
    if output_fmt == "tabular":
        if cluster_samples and len(outputs_list)>0:
            samples_rows = _f_get_samples_rows(outputs_list, samples_list, genotypes_dict, names_dict, biallelic)
            samples_list = f_cluster_samples(samples_rows, biallelic) # from util.py
        # else: samples_list = samples_list
        for sample in samples_list:
            outfile.write("\t"+sample)
    
    outfile.write("\n")
    
    # Rows
    _print_rows(outputs_list, samples_list, variants_dict, genotypes_dict, names_dict,
               output_fmt, biallelic, numeric, outfile)
    
    return

##

## END