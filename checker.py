from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb+srv://prod_read_access_user:LQFtkbsod9d9wuyk@elabsproduction.lagpo.mongodb.net/?retryWrites=true&w=majority&appName=ElabsProduction"
DB_NAME = "itclabs-prod"
COLLECTION_NAME = "el_orders"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Extract field names from the provided Java getters (assuming they should be strings)
EXPECTED_STRING_FIELDS = {
    "scheduler_signature", "testCondition", "reportAmendLabel", "poWise", "headerNote", "stabilityNote",
    "wStateCode", "wUlbCode", "wSampleCode", "wSampleSerial", "samplePackCode", "quantityUnit",
    "prototypeDetailsId", "stabilityCondition", "mode_description", "service_required", "customer_type",
    "discount_type", "revert_comment", "dispatch_number", "dispatch_vendor", "docket_number", "description",
    "sampleDoneBy", "sampleEnvironment", "samplePlan", "quantityRequired", "sampleItem", "reviewer_signature",
    "partyLetterRefNumber", "finalizer_signature", "qa_signature", "dispatcher_signature", "invoicer_signature",
    "micro_biologist_signature", "order_booker_signature", "report_number", "report_series", "report_template",
    "barcodeForFreemarker", "qrcodeForFreemarker", "name", "address", "country", "state", "city", "pincode",
    "zip_code", "mfg_lic_no", "discount_value", "billing_type", "invoicing_type", "letter_ref_no",
    "sample_name", "sample_name_2", "batch_number", "sample_status", "mfg_date", "expiry_date",
    "batch_size", "sample_quantity", "supplied_by", "mfg_by", "brand", "mode", "grade", "declared_value",
    "code_number", "packing_mode", "priority", "surcharge_value", "pi_reference", "sealed_unsealed",
    "signed_unsigned", "sampling_date", "submission_type", "quotation_number", "actual_submission_type",
    "sample_condition", "hold_description", "hold_reason", "unhold_reason", "po_no", "sample_type_details_value",
    "time_in_days", "order_status", "last_status_before_hold", "due_date_change_reason", "review_comment",
    "invoicing_status", "address_line1", "address_line2", "first_name", "last_name", "email", "gst_no",
    "delivery_details", "designation", "tel", "mobile", "phone", "fax", "billing_company", "billing_address",
    "billing_address_line2", "billing_city", "billing_state", "billing_country", "billing_pincode",
    "billing_contact_person", "billing_contact_person_email", "billing_gst", "billing_tel", "billing_mobile",
    "billing_fax", "reporting_company", "reporting_address", "reporting_address_line2", "reporting_city",
    "reporting_state", "reporting_country", "reporting_pincode", "reporting_contact_person",
    "reporting_contact_person_email", "reporting_gst", "reporting_tel", "reporting_mobile", "reporting_fax",
    "other_info", "return_tested", "extra_req", "booking_type", "cancellation_type", "cancellation_reason",
    "previous_status", "batch_no", "return_tested_sample", "sampling_time", "sampling_location",
    "condition_to_maintain", "details", "header_note", "any_other_info", "report_customer_details",
    "report_partc_details", "report_footer_details", "review_note", "review_remarks", "reference_to_sampling",
    "supporting_document", "deviation_from_test_method", "nabl_ulr_no", "analysis_type", "color",
    "rm_details", "project_name", "interim_report_required", "sampling_by", "packSize", "orderScope",
    "mfgLicenseNumber", "otherMfgLicenseNumber", "sampleCondition", "statusOfHold", "statusOfCancellation",
    "sampleGroup", "productGroup", "letterSampleRef", "letterRefDate", "sampler", "barcode_str",
    "sampleRemark", "vendor", "invoiceGenerationStatus", "reportNumberOrg", "sampleSubmission",
    "productLocation", "orderMailStatus", "reportMailStatus", "remarkReviewReason", "reportAmendmentReason",
    "amend_series", "compliance_statement_required", "report_with_header", "report_with_equipment_column",
    "report_with_signature", "report_with_limit", "report_with_accreditation", "environmentCondition"
}

def validate_string_fields():
    incorrect_docs = []
    projection_fields = {field: 1 for field in EXPECTED_STRING_FIELDS}  # Fetch only relevant fields

    cursor = collection.find({}, projection_fields)  # Scan all documents

    for doc in cursor:
        incorrect_fields = {}

        for field in EXPECTED_STRING_FIELDS:
            if field in doc:
                actual_value = doc[field]
                actual_type = type(actual_value)

                # Check if a string field is mistakenly stored as a float or other data type
                if not isinstance(actual_value, str):
                    incorrect_fields[field] = f"{actual_type.__name__} (should be str)"

        if incorrect_fields:
            incorrect_docs.append({"_id": doc["_id"], "incorrect_fields": incorrect_fields})

    # Print incorrect documents
    if incorrect_docs:
        for item in incorrect_docs:
            print(f"Document ID: {item['_id']} has incorrect fields: {item['incorrect_fields']}")
    else:
        print("No incorrect string fields found.")

# Run the function
validate_string_fields()
