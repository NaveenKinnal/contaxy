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
import DeploymentCompute from './DeploymentCompute';
import ExtensionType from './ExtensionType';

/**
 * The ExtensionInput model module.
 * @module model/ExtensionInput
 * @version 0.0.16
 */
class ExtensionInput {
  /**
   * Constructs a new <code>ExtensionInput</code>.
   * @alias module:model/ExtensionInput
   * @param containerImage {String} The container image used for this deployment.
   */
  constructor(containerImage) {
    ExtensionInput.initialize(this, containerImage);
  }

  /**
   * Initializes the fields of this object.
   * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
   * Only for internal use.
   */
  static initialize(obj, containerImage) {
    obj['container_image'] = containerImage;
  }

  /**
   * Constructs a <code>ExtensionInput</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/ExtensionInput} obj Optional instance to populate.
   * @return {module:model/ExtensionInput} The populated <code>ExtensionInput</code> instance.
   */
  static constructFromObject(data, obj) {
    if (data) {
      obj = obj || new ExtensionInput();

      if (data.hasOwnProperty('capabilities')) {
        obj['capabilities'] = ApiClient.convertToType(data['capabilities'], [
          'String',
        ]);
      }
      if (data.hasOwnProperty('api_extension_endpoint')) {
        obj['api_extension_endpoint'] = ApiClient.convertToType(
          data['api_extension_endpoint'],
          'String'
        );
      }
      if (data.hasOwnProperty('ui_extension_endpoint')) {
        obj['ui_extension_endpoint'] = ApiClient.convertToType(
          data['ui_extension_endpoint'],
          'String'
        );
      }
      if (data.hasOwnProperty('extension_type')) {
        obj['extension_type'] = ApiClient.convertToType(
          data['extension_type'],
          ExtensionType
        );
      }
      if (data.hasOwnProperty('container_image')) {
        obj['container_image'] = ApiClient.convertToType(
          data['container_image'],
          'String'
        );
      }
      if (data.hasOwnProperty('parameters')) {
        obj['parameters'] = ApiClient.convertToType(data['parameters'], {
          String: 'String',
        });
      }
      if (data.hasOwnProperty('compute')) {
        obj['compute'] = ApiClient.convertToType(
          data['compute'],
          DeploymentCompute
        );
      }
      if (data.hasOwnProperty('command')) {
        obj['command'] = ApiClient.convertToType(data['command'], ['String']);
      }
      if (data.hasOwnProperty('args')) {
        obj['args'] = ApiClient.convertToType(data['args'], ['String']);
      }
      if (data.hasOwnProperty('requirements')) {
        obj['requirements'] = ApiClient.convertToType(data['requirements'], [
          'String',
        ]);
      }
      if (data.hasOwnProperty('endpoints')) {
        obj['endpoints'] = ApiClient.convertToType(data['endpoints'], [
          'String',
        ]);
      }
      if (data.hasOwnProperty('display_name')) {
        obj['display_name'] = ApiClient.convertToType(
          data['display_name'],
          'String'
        );
      }
      if (data.hasOwnProperty('description')) {
        obj['description'] = ApiClient.convertToType(
          data['description'],
          'String'
        );
      }
      if (data.hasOwnProperty('icon')) {
        obj['icon'] = ApiClient.convertToType(data['icon'], 'String');
      }
      if (data.hasOwnProperty('metadata')) {
        obj['metadata'] = ApiClient.convertToType(data['metadata'], {
          String: 'String',
        });
      }
      if (data.hasOwnProperty('disabled')) {
        obj['disabled'] = ApiClient.convertToType(data['disabled'], 'Boolean');
      }
      if (data.hasOwnProperty('graphql_endpoint')) {
        obj['graphql_endpoint'] = ApiClient.convertToType(
          data['graphql_endpoint'],
          'String'
        );
      }
      if (data.hasOwnProperty('openapi_endpoint')) {
        obj['openapi_endpoint'] = ApiClient.convertToType(
          data['openapi_endpoint'],
          'String'
        );
      }
      if (data.hasOwnProperty('health_endpoint')) {
        obj['health_endpoint'] = ApiClient.convertToType(
          data['health_endpoint'],
          'String'
        );
      }
      if (data.hasOwnProperty('idle_timeout')) {
        obj['idle_timeout'] = ApiClient.convertToType(
          data['idle_timeout'],
          'Number'
        );
      }
      if (data.hasOwnProperty('clear_volume_on_stop')) {
        obj['clear_volume_on_stop'] = ApiClient.convertToType(
          data['clear_volume_on_stop'],
          'Boolean'
        );
      }
      if (data.hasOwnProperty('is_stopped')) {
        obj['is_stopped'] = ApiClient.convertToType(
          data['is_stopped'],
          'Boolean'
        );
      }
    }
    return obj;
  }
}

/**
 * List of capabilities implemented by this extension.
 * @member {Array.<String>} capabilities
 */
ExtensionInput.prototype['capabilities'] = undefined;

/**
 * The endpoint base URL that implements the API operation stated in the capabilities property.
 * @member {String} api_extension_endpoint
 */
ExtensionInput.prototype['api_extension_endpoint'] = undefined;

/**
 * The endpoint instruction that provide a Web UI. If this is provided, the extension will be integrated into the UI.
 * @member {String} ui_extension_endpoint
 */
ExtensionInput.prototype['ui_extension_endpoint'] = undefined;

/**
 * The type of the extension.
 * @member {module:model/ExtensionType} extension_type
 */
ExtensionInput.prototype['extension_type'] = undefined;

/**
 * The container image used for this deployment.
 * @member {String} container_image
 */
ExtensionInput.prototype['container_image'] = undefined;

/**
 * Parameters (environment variables) for this deployment.
 * @member {Object.<String, String>} parameters
 */
ExtensionInput.prototype['parameters'] = undefined;

/**
 * Compute instructions and limitations for this deployment.
 * @member {module:model/DeploymentCompute} compute
 */
ExtensionInput.prototype['compute'] = undefined;

/**
 * Command to run within the deployment. This overwrites the existing docker ENTRYPOINT.
 * @member {Array.<String>} command
 */
ExtensionInput.prototype['command'] = undefined;

/**
 * Arguments to the command/entrypoint. This overwrites the existing docker CMD.
 * @member {Array.<String>} args
 */
ExtensionInput.prototype['args'] = undefined;

/**
 * Additional requirements for deployment.
 * @member {Array.<String>} requirements
 */
ExtensionInput.prototype['requirements'] = undefined;

/**
 * A list of HTTP endpoints that can be accessed. This should always have an internal port and can include additional instructions, such as the URL path.
 * @member {Array.<String>} endpoints
 */
ExtensionInput.prototype['endpoints'] = undefined;

/**
 * A user-defined human-readable name of the resource. The name can be up to 128 characters long and can consist of any UTF-8 character.
 * @member {String} display_name
 */
ExtensionInput.prototype['display_name'] = undefined;

/**
 * A user-defined short description about the resource. Can consist of any UTF-8 character.
 * @member {String} description
 * @default ''
 */
ExtensionInput.prototype['description'] = '';

/**
 * Identifier or image URL used for displaying this resource.
 * @member {String} icon
 */
ExtensionInput.prototype['icon'] = undefined;

/**
 * A collection of arbitrary key-value pairs associated with this resource that does not need predefined structure. Enable third-party integrations to decorate objects with additional metadata for their own use.
 * @member {Object.<String, String>} metadata
 */
ExtensionInput.prototype['metadata'] = undefined;

/**
 * Allows to disable a resource without requiring deletion. A disabled resource is not shown and not accessible.
 * @member {Boolean} disabled
 * @default false
 */
ExtensionInput.prototype['disabled'] = false;

/**
 * GraphQL endpoint.
 * @member {String} graphql_endpoint
 */
ExtensionInput.prototype['graphql_endpoint'] = undefined;

/**
 * Endpoint that prorvides an OpenAPI schema definition..
 * @member {String} openapi_endpoint
 */
ExtensionInput.prototype['openapi_endpoint'] = undefined;

/**
 * The endpoint instruction that can be used for checking the deployment health.
 * @member {String} health_endpoint
 */
ExtensionInput.prototype['health_endpoint'] = undefined;

/**
 * Time after which the service is considered idling and will be stopped during the next idle check.If set to None, the service will never be considered idling.Can be specified as seconds or ISO 8601 time delta.
 * @member {Number} idle_timeout
 */
ExtensionInput.prototype['idle_timeout'] = undefined;

/**
 * If set to true, any volume attached to the service be deleted when the service is stopped.This means all persisted data will be cleared on service stop.
 * @member {Boolean} clear_volume_on_stop
 * @default false
 */
ExtensionInput.prototype['clear_volume_on_stop'] = false;

/**
 * If set to true, the service will be created in the DB but not started. The service status will be 'stopped'.
 * @member {Boolean} is_stopped
 * @default false
 */
ExtensionInput.prototype['is_stopped'] = false;

export default ExtensionInput;
