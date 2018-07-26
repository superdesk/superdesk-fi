/**
 * This is the default configuration file for the Superdesk application. By default,
 * the app will use the file with the name "superdesk.config.js" found in the current
 * working directory, but other files may also be specified using relative paths with
 * the SUPERDESK_CONFIG environment variable or the grunt --config flag.
 */
module.exports = function(grunt) {
    return {
        apps: [],
        defaultRoute: '/workspace/personal',
        validatorMediaMetadata: {
            headline: {
                required: true
            },
            alt_text: {
                required: true
            },
            description_text: {
                required: true
            },
            copyrightholder: {
                required: false
            },
            byline: {
                required: true
            },
            usageterms: {
                required: false
            },
            copyrightnotice: {
                required: false
            }
        },

        list: {
            priority: [
                'priority',
                'urgency'
            ],
            firstLine: [
                'wordcount',
                'slugline',
                'highlights',
                'markedDesks',
                'associations',
                'publish_queue_errors',
                'headline',
                'versioncreated'
            ],
            secondLine: [
                'language',
                'profile',
                'state',
                'embargo',
                'update',
                'takekey',
                'signal',
                'broadcast',
                'flags',
                'updated',
                'category',
                'expiry',
                'desk',
                'fetchedDesk'
            ]
        },

        langOverride: {
            'en': {
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY',
                'Subject': 'Theme',
                'SUBJECT': 'THEME',
                'Genre': 'Content Type',
                'GENRE': 'CONTENT TYPE',
                'Place': 'Compliance Country',
                'PLACE': 'COMPLIANCE COUNTRY',
                'Footer': 'Foot Note',
                'FOOTER': 'FOOT NOTE',
                'Urgency': 'Featured Content',
                'URGENCY': 'FEATURED CONTENT',
                'Authors': 'Contributors',
                'AUTHORS': 'CONTRIBUTORS'
            },

            'en_GB': {
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY',
                'Subject': 'Theme',
                'SUBJECT': 'THEME',
                'Genre': 'Content Type',
                'GENRE': 'CONTENT TYPE',
                'Place': 'Compliance Country',
                'PLACE': 'COMPLIANCE COUNTRY',
                'Footer': 'Foot Note',
                'FOOTER': 'FOOT NOTE',
                'Urgency': 'Featured Content',
                'URGENCY': 'FEATURED CONTENT',
                'Authors': 'Contributors',
                'AUTHORS': 'CONTRIBUTORS'
            },

            'en_US': {
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY',
                'Subject': 'Theme',
                'SUBJECT': 'THEME',
                'Genre': 'Content Type',
                'GENRE': 'CONTENT TYPE',
                'Place': 'Compliance Country',
                'PLACE': 'COMPLIANCE COUNTRY',
                'Footer': 'Foot Note',
                'FOOTER': 'FOOT NOTE',
                'Urgency': 'Featured Content',
                'URGENCY': 'FEATURED CONTENT',
                'Authors': 'Contributors',
                'AUTHORS': 'CONTRIBUTORS'
            },

            'en_AU': {
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY',
                'Subject': 'Theme',
                'SUBJECT': 'THEME',
                'Genre': 'Content Type',
                'GENRE': 'CONTENT TYPE',
                'Place': 'Compliance Country',
                'PLACE': 'COMPLIANCE COUNTRY',
                'Footer': 'Foot Note',
                'FOOTER': 'FOOT NOTE',
                'Urgency': 'Featured Content',
                'URGENCY': 'FEATURED CONTENT',
                'Authors': 'Contributors',
                'AUTHORS': 'CONTRIBUTORS'
            }
        },

        infoRemovedFields: {
            language: true
        },

        defaultRoute: '/workspace/monitoring',

        features: {
            preview: 1,
            legal_archive: 1,
            swimlane: {columnsLimit: 4},
            editor3: true,
            editorHighlights: true,
            hideCreatePackage: false,
            noMissingLink: true,
            qumu: true,
            noPublishOnAuthoringDesk: true
        },
        workspace: {},
        profile: {
            jid: false,
            place: false,
            category: false
        },

        search_cvs: [
            {id: 'genre', name:'Genre', field: 'genre', list: 'genre_custom'},
            {id: 'place', name:'Place', field: 'place', list: 'place_custom'},
            {id: 'subject', name:'Subject', field: 'subject', list: 'subject_custom'},
            {id: 'franchise', name:'Franchise', field: 'subject', list: 'franchise'}
        ],

        search: {
            'slugline': 1,
            'headline': 1,
            'unique_name': 0,
            'story_text': 0,
            'byline': 1,
            'keywords': 0,
            'creator': 1,
            'from_desk': 1,
            'to_desk': 1,
            'spike': 1,
            'ingest_provider': 0,
            'marked_desks': 0,
            'scheduled': 1
        },
    };
};
