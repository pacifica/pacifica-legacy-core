#!/usr/bin/python

def schema_get(schema):
	all = {
		'simple_item': """
{
	"settings": {
		"index": {
			"number_of_shards": 10,
			"number_of_replicas": 0
		},
		"analysis": {
			"analyzer": {
				"a1": {
					"type": "custom",
					"tokenizer": "standard",
					"filter" : ["lowercase", "my_filter"]
				}
			},
			"filter": {
				"my_filter": {
					"type": "nGram",
					"min_gram": 2,
					"max_gram": 20
				}
			}
		}
	},
	"mappings": {
		"simple_items" : {
			"_source": {"enabled": true},
			"_all": {
				"type": "string",
				"null_value": "na",
				"index": "analyzed",
				"index_analyzer": "a1",
				"search_analyzer": "default"
			},
			"properties": {
				"groups.Tag": {
					"type": "string",
					"index_analyzer": "whitespace",
					"search_analyzer": "whitespace"
				},
				"groups.gov_pnnl_emsl_pacifica_generic_publication": {
					"type" : "multi_field",
					"fields" : {
						"groups.gov_pnnl_emsl_pacifica_generic_publication": {
							"type": "string"
						},
						"untouched": {
							"type": "string",
							"null_value": "na",
							"index": "analyzed",
							"analyzer": "keyword"
						}
					}
				},
				"extended_metadata": {
					"dynamic": true,
					"properties": { 
						"gov_pnnl_erica/irn": {
							"dynamic": true,
							"properties": {
								"id": {
									"type" : "multi_field",
									"fields" : {
										"id": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								}
							}
						},
						"gov_pnnl_emsl_instrument": {
							"dynamic": true,
							"properties": {
								"name": {
									"type" : "multi_field",
									"fields" : {
										"name": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								}
							}
						},
						"gov_pnnl_emsl_dms_dataset": {
							"dynamic": true,
							"properties": {
								"name": {
									"type" : "multi_field",
									"fields" : {
										"name": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								}
							}
						},
						"gov_pnnl_emsl_dms_datapackage": {
							"dynamic": true,
							"properties": {
								"name": {
									"type" : "multi_field",
									"fields" : {
										"name": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								}
							}
						},
						"gov_pnnl_emsl_dms_campaign": {
							"dynamic": true,
							"properties": {
								"name": {
									"type" : "multi_field",
									"fields" : {
										"name": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								}
							}
						},
						"gov_pnnl_emsl_dms_experiment": {
							"dynamic": true,
							"properties": {
								"name": {
									"type" : "multi_field",
									"fields" : {
										"name": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								}
							}
						},
						"gov_pnnl_emsl_dms_analysisjob": {
							"dynamic": true,
							"properties": {
								"name": {
									"type" : "multi_field",
									"fields" : {
										"name": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								},
								"tool": {
									"dynamic": true,
									"properties": {
										"name": {
											"type" : "multi_field",
											"fields" : {
												"name": {
													"type": "string"
												},
												"untouched": {
													"type": "string",
													"null_value": "na",
													"index": "analyzed",
													"analyzer": "keyword"
												}
											}
										}
									}
								}
							}
						}
					}
				},
				"submittername": {
					"type" : "multi_field",
					"fields" : {
						"submittername": {
							"type": "string"
						},
						"untouched": {
							"type": "string",
							"null_value": "na",
							"index": "analyzed",
							"analyzer": "keyword"
						}
					}
				}
			}
		}
	}
}""",
	'proposal': """
{
	"settings": {
		"index": {
			"number_of_shards": 5,
			"number_of_replicas": 0
		},
		"analysis": {
			"analyzer": {
				"a1": {
					"type": "custom",
					"tokenizer": "standard",
					"filter" : ["lowercase", "my_filter"]
				}
			},
			"filter": {
				"my_filter": {
					"type": "nGram",
					"min_gram": 2,
					"max_gram": 20
				}
			}
		}
	},
	"mappings": {
		"proposal" : {
			"_source": {"enabled": true},
			"_all": {
				"type": "string",
				"null_value": "na",
				"index": "analyzed",
				"index_analyzer": "a1",
				"search_analyzer": "default"
			},
			"properties": {
				"instrument_names" : {
					"type": "string",
					"null_value": "na",
					"index": "analyzed",
					"analyzer": "keyword"
				},
				"email_addresses" : {
					"type": "string",
					"null_value": "na",
					"index": "analyzed",
					"analyzer": "keyword"
				},
				"person_names" : {
					"type" : "multi_field",
					"fields" : {
						"person_names": {
							"type": "string"
						},
						"untouched": {
							"type": "string",
							"null_value": "na",
							"index": "analyzed",
							"analyzer": "keyword"
						}
					}
				},
				"accepted_date" : {
					"type" : "date",
					"format" : "YYYY-MM-dd"
				}
			}
		}
	}
}""",
	'predicate': """
{
	"settings": {
		"index": {
			"number_of_shards": 5,
			"number_of_replicas": 0
		},
		"analysis": {
			"analyzer": {
				"a1": {
					"type": "custom",
					"tokenizer": "standard",
					"filter" : ["lowercase", "my_filter"]
				}
			},
			"filter": {
				"my_filter": {
					"type": "nGram",
					"min_gram": 2,
					"max_gram": 20
				}
			}
		}
	},
	"mappings": {
		"local_predicate" : {
			"_source": {"enabled": true},
			"_all": {
				"type": "string",
				"null_value": "na",
				"index": "analyzed",
				"index_analyzer": "a1",
				"search_analyzer": "default"
			},
			"properties": {
				"description" : {
					"type" : "object",
					"properties": {
						"short" : {
							"type" : "multi_field",
							"fields" : {
								"short": {
									"type": "string"
								},
								"untouched": {
									"type": "string",
									"null_value": "na",
									"index": "analyzed",
									"analyzer": "keyword"
								}
							}
						},
						"long" : {
							"type" : "multi_field",
							"fields" : {
								"long": {
									"type": "string"
								},
								"untouched": {
									"type": "string",
									"null_value": "na",
									"index": "analyzed",
									"analyzer": "keyword"
								}
							}
						}
					}
				},
				"submitter" : {
					"type" : "object",
					"properties": {
						"name" : {
							"type" : "multi_field",
							"fields" : {
								"name": {
									"type": "string"
								},
								"untouched": {
									"type": "string",
									"null_value": "na",
									"index": "analyzed",
									"analyzer": "keyword"
								}
							}
						}
					}
				}
			}
		}
	}
}""",
	'released_publications': """
{
	"settings": {
		"index": {
			"number_of_shards": 5,
			"number_of_replicas": 0
		},
		"analysis": {
			"analyzer": {
				"a1": {
					"type": "custom",
					"tokenizer": "standard",
					"filter" : ["lowercase", "my_filter"]
				}
			},
			"filter": {
				"my_filter": {
					"type": "nGram",
					"min_gram": 2,
					"max_gram": 20
				}
			}
		}
	},
	"mappings": {
		"released_publications" : {
			"_source": {"enabled": true},
			"_all": {
				"type": "string",
				"null_value": "na",
				"index": "analyzed",
				"index_analyzer": "a1",
				"search_analyzer": "default"
			},
			"properties": {
				"contributors" : {
					"dynamic": true,
					"properties": {
						"institution": {
							"type": "multi_field",
							"fields": {
								"institution": {
									"type": "string"
								},
								"untouched": {
									"type": "string",
									"null_value": "na",
									"index": "analyzed",
									"analyzer": "keyword"
								}
							}
						}
					}
				},
				"publication_info": {
					"dynamic": true,
					"properties": {
						"publication": {
							"dynamic": true,
							"properties": {
								"journal_name": {
									"type": "multi_field",
									"fields": {
										"journal_name": {
											"type": "string"
										},
										"untouched": {
											"type": "string",
											"null_value": "na",
											"index": "analyzed",
											"analyzer": "keyword"
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}"""
	}
	return all[schema]

