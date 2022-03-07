/**
 * Contaxy API
 * Functionality to create and manage projects, services, jobs, and files.
 *
 * The version of the OpenAPI document: 0.0.10
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

import ApiClient from '../ApiClient';
/**
 * Enum class DeploymentStatus.
 * @enum {}
 * @readonly
 */
export default class DeploymentStatus {
  /**
   * value: "pending"
   * @const
   */
  pending = 'pending';

  /**
   * value: "running"
   * @const
   */
  running = 'running';

  /**
   * value: "succeeded"
   * @const
   */
  succeeded = 'succeeded';

  /**
   * value: "failed"
   * @const
   */
  failed = 'failed';

  /**
   * value: "terminating"
   * @const
   */
  terminating = 'terminating';

  /**
   * value: "stopped"
   * @const
   */
  stopped = 'stopped';

  /**
   * value: "unknown"
   * @const
   */
  unknown = 'unknown';

  /**
   * Returns a <code>DeploymentStatus</code> enum value from a Javascript object name.
   * @param {Object} data The plain JavaScript object containing the name of the enum value.
   * @return {module:model/DeploymentStatus} The enum <code>DeploymentStatus</code> value.
   */
  static constructFromObject(object) {
    return object;
  }
}
