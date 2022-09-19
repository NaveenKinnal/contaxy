/**
 * Contaxy API
 * Functionality to create and manage projects, services, jobs, and files.
 *
 * The version of the OpenAPI document: 0.0.20
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

import ApiClient from '../ApiClient';
import Compute from './Compute';

/**
 * The ServiceUpdate model module.
 * @module model/ServiceUpdate
 * @version 0.0.20
 */
class ServiceUpdate {
    /**
     * Constructs a new <code>ServiceUpdate</code>.
     * @alias module:model/ServiceUpdate
     */
    constructor() { 
        
        ServiceUpdate.initialize(this);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj) { 
    }

    /**
     * Constructs a <code>ServiceUpdate</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/ServiceUpdate} obj Optional instance to populate.
     * @return {module:model/ServiceUpdate} The populated <code>ServiceUpdate</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new ServiceUpdate();

            if (data.hasOwnProperty('container_image')) {
                obj['container_image'] = ApiClient.convertToType(data['container_image'], 'String');
            }
            if (data.hasOwnProperty('parameters')) {
                obj['parameters'] = ApiClient.convertToType(data['parameters'], {'String': 'String'});
            }
            if (data.hasOwnProperty('compute')) {
                obj['compute'] = Compute.constructFromObject(data['compute']);
            }
            if (data.hasOwnProperty('command')) {
                obj['command'] = ApiClient.convertToType(data['command'], ['String']);
            }
            if (data.hasOwnProperty('args')) {
                obj['args'] = ApiClient.convertToType(data['args'], ['String']);
            }
            if (data.hasOwnProperty('requirements')) {
                obj['requirements'] = ApiClient.convertToType(data['requirements'], ['String']);
            }
            if (data.hasOwnProperty('endpoints')) {
                obj['endpoints'] = ApiClient.convertToType(data['endpoints'], ['String']);
            }
            if (data.hasOwnProperty('display_name')) {
                obj['display_name'] = ApiClient.convertToType(data['display_name'], 'String');
            }
            if (data.hasOwnProperty('description')) {
                obj['description'] = ApiClient.convertToType(data['description'], 'String');
            }
            if (data.hasOwnProperty('icon')) {
                obj['icon'] = ApiClient.convertToType(data['icon'], 'String');
            }
            if (data.hasOwnProperty('metadata')) {
                obj['metadata'] = ApiClient.convertToType(data['metadata'], {'String': 'String'});
            }
            if (data.hasOwnProperty('disabled')) {
                obj['disabled'] = ApiClient.convertToType(data['disabled'], 'Boolean');
            }
            if (data.hasOwnProperty('graphql_endpoint')) {
                obj['graphql_endpoint'] = ApiClient.convertToType(data['graphql_endpoint'], 'String');
            }
            if (data.hasOwnProperty('openapi_endpoint')) {
                obj['openapi_endpoint'] = ApiClient.convertToType(data['openapi_endpoint'], 'String');
            }
            if (data.hasOwnProperty('health_endpoint')) {
                obj['health_endpoint'] = ApiClient.convertToType(data['health_endpoint'], 'String');
            }
            if (data.hasOwnProperty('idle_timeout')) {
                obj['idle_timeout'] = ApiClient.convertToType(data['idle_timeout'], 'Number');
            }
            if (data.hasOwnProperty('clear_volume_on_stop')) {
                obj['clear_volume_on_stop'] = ApiClient.convertToType(data['clear_volume_on_stop'], 'Boolean');
            }
            if (data.hasOwnProperty('is_stopped')) {
                obj['is_stopped'] = ApiClient.convertToType(data['is_stopped'], 'Boolean');
            }
        }
        return obj;
    }


}

/**
 * The container image used for this deployment.
 * @member {String} container_image
 * @default ''
 */
ServiceUpdate.prototype['container_image'] = '';

/**
 * Parmeters (enviornment variables) for this deployment.
 * @member {Object.<String, String>} parameters
 */
ServiceUpdate.prototype['parameters'] = undefined;

/**
 * @member {module:model/Compute} compute
 */
ServiceUpdate.prototype['compute'] = undefined;

/**
 * Command to run within the deployment. This overwrites the existing docker ENTRYPOINT.
 * @member {Array.<String>} command
 */
ServiceUpdate.prototype['command'] = undefined;

/**
 * Arguments to the command/entrypoint. This overwrites the existing docker CMD.
 * @member {Array.<String>} args
 */
ServiceUpdate.prototype['args'] = undefined;

/**
 * Additional requirements for deployment.
 * @member {Array.<String>} requirements
 */
ServiceUpdate.prototype['requirements'] = undefined;

/**
 * A list of HTTP endpoints that can be accessed. This should always have an internal port and can include additional instructions, such as the URL path.
 * @member {Array.<String>} endpoints
 */
ServiceUpdate.prototype['endpoints'] = undefined;

/**
 * A user-defined human-readable name of the resource. The name can be up to 128 characters long and can consist of any UTF-8 character.
 * @member {String} display_name
 */
ServiceUpdate.prototype['display_name'] = undefined;

/**
 * A user-defined short description about the resource. Can consist of any UTF-8 character.
 * @member {String} description
 * @default ''
 */
ServiceUpdate.prototype['description'] = '';

/**
 * Identifier or image URL used for displaying this resource.
 * @member {String} icon
 */
ServiceUpdate.prototype['icon'] = undefined;

/**
 * A collection of arbitrary key-value pairs associated with this resource that does not need predefined structure. Enable third-party integrations to decorate objects with additional metadata for their own use.
 * @member {Object.<String, String>} metadata
 */
ServiceUpdate.prototype['metadata'] = undefined;

/**
 * Allows to disable a resource without requiring deletion. A disabled resource is not shown and not accessible.
 * @member {Boolean} disabled
 * @default false
 */
ServiceUpdate.prototype['disabled'] = false;

/**
 * GraphQL endpoint.
 * @member {String} graphql_endpoint
 */
ServiceUpdate.prototype['graphql_endpoint'] = undefined;

/**
 * Endpoint that prorvides an OpenAPI schema definition..
 * @member {String} openapi_endpoint
 */
ServiceUpdate.prototype['openapi_endpoint'] = undefined;

/**
 * The endpoint instruction that can be used for checking the deployment health.
 * @member {String} health_endpoint
 */
ServiceUpdate.prototype['health_endpoint'] = undefined;

/**
 * Time after which the service is considered idling and will be stopped during the next idle check.If set to None, the service will never be considered idling.Can be specified as seconds or ISO 8601 time delta.
 * @member {Number} idle_timeout
 */
ServiceUpdate.prototype['idle_timeout'] = undefined;

/**
 * If set to true, any volume attached to the service be deleted when the service is stopped.This means all persisted data will be cleared on service stop.
 * @member {Boolean} clear_volume_on_stop
 * @default false
 */
ServiceUpdate.prototype['clear_volume_on_stop'] = false;

/**
 * If set to true, the service will be created in the DB but not started. The service status will be 'stopped'.
 * @member {Boolean} is_stopped
 * @default false
 */
ServiceUpdate.prototype['is_stopped'] = false;






export default ServiceUpdate;

