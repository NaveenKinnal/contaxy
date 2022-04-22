/**
 * Contaxy API
 * Functionality to create and manage projects, services, jobs, and files.
 *
 * The version of the OpenAPI document: 0.0.16
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

import ApiClient from '../ApiClient';

/**
 * The BodyUploadFileProjectsProjectIdFilesFileKeyPost model module.
 * @module model/BodyUploadFileProjectsProjectIdFilesFileKeyPost
 * @version 0.0.16
 */
class BodyUploadFileProjectsProjectIdFilesFileKeyPost {
  /**
   * Constructs a new <code>BodyUploadFileProjectsProjectIdFilesFileKeyPost</code>.
   * @alias module:model/BodyUploadFileProjectsProjectIdFilesFileKeyPost
   * @param file {File}
   */
  constructor(file) {
    BodyUploadFileProjectsProjectIdFilesFileKeyPost.initialize(this, file);
  }

  /**
   * Initializes the fields of this object.
   * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
   * Only for internal use.
   */
  static initialize(obj, file) {
    obj['file'] = file;
  }

  /**
   * Constructs a <code>BodyUploadFileProjectsProjectIdFilesFileKeyPost</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/BodyUploadFileProjectsProjectIdFilesFileKeyPost} obj Optional instance to populate.
   * @return {module:model/BodyUploadFileProjectsProjectIdFilesFileKeyPost} The populated <code>BodyUploadFileProjectsProjectIdFilesFileKeyPost</code> instance.
   */
  static constructFromObject(data, obj) {
    if (data) {
      obj = obj || new BodyUploadFileProjectsProjectIdFilesFileKeyPost();

      if (data.hasOwnProperty('file')) {
        obj['file'] = ApiClient.convertToType(data['file'], File);
      }
    }
    return obj;
  }
}

/**
 * @member {File} file
 */
BodyUploadFileProjectsProjectIdFilesFileKeyPost.prototype['file'] = undefined;

export default BodyUploadFileProjectsProjectIdFilesFileKeyPost;
