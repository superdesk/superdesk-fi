# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : Jérôme
# Creation: 2018-12-18 14:32

from superdesk.commands.data_updates import DataUpdate
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE
from superdesk import get_resource_service


to_kill = [
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T16:51:07.625309:953b67f5-5c48-430a-adf5-97a8c981e63a",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:49:20.549929:2c7ff2af-19e0-4eee-957d-9c3f4bae563a",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T19:04:33.073197:25474838-c125-4d0f-ac12-0c58ff89dd42",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T16:38:43.082837:eb9a5d0e-964e-4fb7-ba43-e3711e1ffb4d",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:32:34.607668:d6da7442-11d4-4123-9465-92b58caa4631",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-13T14:01:15.675487:49c2a498-dc04-4c4a-811a-00a3515ab9c3",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:17:24.545056:f35e3064-4649-4af2-85dc-c0ca9edaa79e",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T12:48:03.607436:a6415fc9-ef47-4699-b242-8547f1d4fd87",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:52:47.881153:52c21890-2dd6-449e-95ba-6894d3be3364",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T16:52:28.111491:8f51b238-3184-47dc-b0c8-da98ae6b99cb",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-13T14:06:28.035049:6fd457d4-bb3a-40f9-8e45-2a5f08c6367f",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:52:48.965142:dd97ee81-2646-4db6-ad20-14e339085739",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:17:25.471683:0620da09-6867-4407-a378-dde264e20614",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T19:04:34.091994:26f6d494-5f3e-4abe-be45-c18d66148871",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:49:21.597036:7c272fee-04bb-4e09-8147-f422ae618b88",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T08:00:46.746231:4dd8581e-872e-4985-8276-e56a5ba4da28",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:32:35.527368:8e3e13ea-e5aa-4c74-a756-f256997d9eef",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:32:34.918491:9463b860-e2a0-4a32-a7e6-e7fab7312ad1",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:49:20.936466:a9f21f4b-63a4-41d1-80ea-8ac51a741dd8",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-13T14:08:34.671533:289f0f89-72cc-4f6b-9c77-b4edbdaf8e2b",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:52:48.302563:49e96c5e-d850-4525-a3b6-4e0ac418b663",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T12:22:00.489247:85ebbb26-4145-4cb8-babc-eeb6307c45cd",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:17:24.855518:b1d9e696-822c-4f80-b9cf-2090a2ac69fc",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T16:42:21.904574:d33a4091-4061-4193-9fb3-58992103271c",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T19:04:33.408621:408acacb-f399-4f70-8a70-b1cf304b364b",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:32:35.088558:c3df21e1-3b83-46f6-b500-12788b62ce26",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T19:04:33.619679:62dbbf71-edcd-4207-b1d9-65c69cea51e1",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:49:21.101430:0accb162-ad3f-4056-bfb3-ac15a7eb4c92",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:17:25.030401:cad5abd9-f8fe-414d-8851-d3b9d616da4f",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:52:48.464635:effed6dd-229e-461f-80c3-bb4f7cfed89e",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-13T14:17:09.415371:50264206-eff2-4b13-bded-1eec7da3462b",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-17T12:04:17.596060:7ebd0c6a-ac0e-4289-adbb-9820aef8b4f7",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:17:25.149901:f2108169-91d6-42d1-b92d-a38c51337580",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T11:28:11.334794:8a67a371-d09a-4447-a795-eb3b1c7dac85",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T19:04:33.772440:ed22c69e-fa6f-447d-b23f-0b61c6930408",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-15T16:46:09.224970:c2366b2b-2664-4901-9258-9ad69be91699",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T16:31:56.698346:6209c7b3-32c0-4707-8821-8e8c8bc6107e",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T08:00:46.616456:969b9367-bf9e-4c7a-8c54-05245517ba9b",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:52:48.609682:dbdfab55-ec31-4230-b29a-8d9138bb5efe",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T11:39:48.012630:74a8f94e-c9c1-456a-a0d0-c5cb7c2d09f7",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:32:35.464312:07f77f7c-9a74-4ffe-b9e7-900fdefdfc77",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:49:21.517696:590dbacd-bea7-44cb-a3dd-9b28f38633e6",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-21T16:49:28.076869:2ab1bcc1-f2db-4d0c-a043-a01ca59bff55",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T19:04:34.016576:2c50815e-55a1-4a4d-94b1-81e7bc48e58a",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:17:25.404195:c23914d0-75f5-4f71-9ef5-b5fe0e3a95b1",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:52:48.895720:9a5326ee-4bad-4cba-85b5-187e6c99ea3c",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T16:47:49.111138:a92908dd-fa6b-493b-997c-cec54d5c427d",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-13T14:30:34.007235:c8627cc3-49e7-46ef-ac75-f74cecf694b8",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-14T09:58:04.733353:99d2511e-7753-4264-b48e-94fa209c4022",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:32:35.163559:562fe7a7-f9bc-485c-bd47-9f79eef69a83",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-23T13:52:48.546709:7a774ddc-64ea-4553-a56e-499229085066",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-17T11:57:50.849069:bcabee71-f1a7-4a89-b571-0e01604594ee",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T19:04:33.707202:2e47d154-f240-4040-9696-f98498d464bb",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-22T18:17:25.098125:0c3b5869-050d-449b-94a3-b750cddd269a",
    "urn:newsml:fidelity-api.superdesk.pro:2017-11-16T13:35:33.689534:25f811bb-dcf3-4dd4-919e-17c94bc5e5af",
]


class DataUpdate(DataUpdate):

    resource = 'archive'

    def forwards(self, collection, mongodb_database):
        archive_service = get_resource_service("archive")
        kill_service = get_resource_service("archive_kill")
        killed = 0
        for item_id in to_kill:
            update = {ITEM_STATE: CONTENT_STATE.KILLED}
            ori_item = archive_service.find_one(None, _id=item_id)
            if ori_item is None:
                print('Can\'t find item "{item_id}", ignoring'.format(item_id=item_id))
                continue
            update['subject'] = subject = ori_item.get('subject', [])
            # we add missing mandatory metadata if needed
            # else killing would fail because of validation
            if not any({d.get('scheme') == 'instprtlsection' for d in subject}):
                subject.append({
                    "scheme": "instprtlsection",
                    "qcode": "instprtlsection:100201",
                    "name": "Edition 1"})
            if not any({d.get('scheme') == 'compliance_checked' for d in subject}):
                subject.append({
                    "parent": None,
                    "qcode": "compliance:yes",
                    "scheme": "compliance_checked",
                    "name": "Yes"})
            if "Perma_URL" not in ori_item.setdefault('extra', {}):
                update["extra"] = ori_item["extra"]
                update["extra"]["Perma_URL"] = "https://invalid.invalid"
            if "disclaimer" not in ori_item['extra']:
                update["extra"] = ori_item["extra"]
                update["extra"]["disclaimer"] = "disclaimer"
            # some summaries are too long, we need to check them to pass validation
            if len(ori_item['extra'].get("Summary") or "") > 450:
                update["extra"]["Summary"] = update["extra"]["Summary"][:450]

            versioncreated = ori_item['versioncreated']

            try:
                kill_service.patch(item_id, update)
            except Exception as e:
                print('Can\'t kill item "{item_id}": {reason}'.format(
                    item_id=item_id, reason=e))
            else:
                print('Item "{item_id}" killed'.format(item_id=item_id))
                killed += 1
                # we now restore original versioncreated as we want item to be expired
                print('restoring original versioncreated')
                try:
                    collection.update({'_id': item_id}, {
                        '$set': {
                            'versioncreated': versioncreated
                        }})
                except Exception as e:
                    print('Can\'t restore versioncreated for item "{item_id}": {reason}'.format(
                        item_id=item_id, reason=e))

        print("{nb} items have been killed".format(nb=killed))
        if killed < len(to_kill):
            print("{nb} items have *not* been killed".format(nb=len(to_kill) - killed))

    def backwards(self, mongodb_collection, mongodb_database):
        pass
