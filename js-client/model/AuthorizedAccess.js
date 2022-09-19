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
import AccessLevel from './AccessLevel';
import AccessToken from './AccessToken';

/**
 * The AuthorizedAccess model module.
 * @module model/AuthorizedAccess
 * @version 0.0.20
 */
class AuthorizedAccess {
    /**
     * Constructs a new <code>AuthorizedAccess</code>.
     * @alias module:model/AuthorizedAccess
     * @param authorizedSubject {String} 
     */
    constructor(authorizedSubject) { 
        
        AuthorizedAccess.initialize(this, authorizedSubject);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, authorizedSubject) { 
        obj['authorized_subject'] = authorizedSubject;
    }

    /**
     * Constructs a <code>AuthorizedAccess</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/AuthorizedAccess} obj Optional instance to populate.
     * @return {module:model/AuthorizedAccess} The populated <code>AuthorizedAccess</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new AuthorizedAccess();

            if (data.hasOwnProperty('authorized_subject')) {
                obj['authorized_subject'] = ApiClient.convertToType(data['authorized_subject'], 'String');
            }
            if (data.hasOwnProperty('resource_name')) {
                obj['resource_name'] = ApiClient.convertToType(data['resource_name'], 'String');
            }
            if (data.hasOwnProperty('access_level')) {
                obj['access_level'] = AccessLevel.constructFromObject(data['access_level']);
            }
            if (data.hasOwnProperty('access_token')) {
                obj['access_token'] = AccessToken.constructFromObject(data['access_token']);
            }
        }
        return obj;
    }


}

/**
 * @member {String} authorized_subject
 */
AuthorizedAccess.prototype['authorized_subject'] = undefined;

/**
 * @member {String} resource_name
 */
AuthorizedAccess.prototype['resource_name'] = undefined;

/**
 * @member {module:model/AccessLevel} access_level
 */
AuthorizedAccess.prototype['access_level'] = undefined;

/**
 * @member {module:model/AccessToken} access_token
 */
AuthorizedAccess.prototype['access_token'] = undefined;






export default AuthorizedAccess;

