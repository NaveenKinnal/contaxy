/**
 * Contaxy API
 * Functionality to create and manage projects, services, jobs, and files.
 *
 * The version of the OpenAPI document: 0.0.4
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

import ApiClient from '../ApiClient';

/**
 * The JsonDocument model module.
 * @module model/JsonDocument
 * @version 0.0.4
 */
class JsonDocument {
  /**
   * Constructs a new <code>JsonDocument</code>.
   * @alias module:model/JsonDocument
   * @param key {String} Unique key of the document.
   * @param jsonValue {String} JSON value of the document.
   */
  constructor(key, jsonValue) {
    JsonDocument.initialize(this, key, jsonValue);
  }

  /**
   * Initializes the fields of this object.
   * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
   * Only for internal use.
   */
  static initialize(obj, key, jsonValue) {
    obj['key'] = key;
    obj['json_value'] = jsonValue;
  }

  /**
   * Constructs a <code>JsonDocument</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/JsonDocument} obj Optional instance to populate.
   * @return {module:model/JsonDocument} The populated <code>JsonDocument</code> instance.
   */
  static constructFromObject(data, obj) {
    if (data) {
      obj = obj || new JsonDocument();

      if (data.hasOwnProperty('key')) {
        obj['key'] = ApiClient.convertToType(data['key'], 'String');
      }
      if (data.hasOwnProperty('json_value')) {
        obj['json_value'] = ApiClient.convertToType(
          data['json_value'],
          'String'
        );
      }
      if (data.hasOwnProperty('created_at')) {
        obj['created_at'] = ApiClient.convertToType(data['created_at'], 'Date');
      }
      if (data.hasOwnProperty('created_by')) {
        obj['created_by'] = ApiClient.convertToType(
          data['created_by'],
          'String'
        );
      }
      if (data.hasOwnProperty('updated_at')) {
        obj['updated_at'] = ApiClient.convertToType(data['updated_at'], 'Date');
      }
      if (data.hasOwnProperty('updated_by')) {
        obj['updated_by'] = ApiClient.convertToType(
          data['updated_by'],
          'String'
        );
      }
    }
    return obj;
  }
}

/**
 * Unique key of the document.
 * @member {String} key
 */
JsonDocument.prototype['key'] = undefined;

/**
 * JSON value of the document.
 * @member {String} json_value
 */
JsonDocument.prototype['json_value'] = undefined;

/**
 * Creation date of the document.
 * @member {Date} created_at
 */
JsonDocument.prototype['created_at'] = undefined;

/**
 * ID of the user that created this document.
 * @member {String} created_by
 */
JsonDocument.prototype['created_by'] = undefined;

/**
 * Last date at which the document was updated.
 * @member {Date} updated_at
 */
JsonDocument.prototype['updated_at'] = undefined;

/**
 * ID of the user that has last updated this document.
 * @member {String} updated_by
 */
JsonDocument.prototype['updated_by'] = undefined;

export default JsonDocument;
