from django.test import TestCase, Client

class StreamViewTest(TestCase):
    def test_get_success(self):
        client = Client()
        response = client.get('/music/1')
from django.db.models import F

from .models import *


clnt = Client()



class MainViewTest(TestCase):

    def test_first_req_contents(self):

        res = clnt.get('/music/main')

        self.assertEqual(
            res.status_code,
            200
        )

        self.assertEqual(
            res.json()[
                'contents'
            ],
            [
                {
                    'collection':Collection.objects
                    .filter(
                        id=i
                    ).values(
                        'name'
                    ).first()[
                        'name'
                    ],
                    'elements':
                    list(
                        Collection.objects.prefetch_related(
                            'playlist_set'
                        ).filter(
                            id=i
                        ).annotate(
                            list_id = F('playlist__id'),
                            list_name = F('playlist__name'),
                            list_thumb = F('playlist__thumbnail_id__url'),
                            list_type = F('playlist__type_id__name'),
                            list_artist = F('playlist__artist')
                        ).values(
                            'list_id',
                            'list_name',
                            'list_thumb',
                            'list_type',
                            'list_artist'
                        )
                    )
                }
                for i in [1,7,13]
            ]
        )



    def test_first_req_infra_elements(self):

        res = clnt.get('/music/main')

        self.assertEqual(
            res.json()[
                'main_thumb'
            ],
            Collection.objects.filter(
                id = 1
            ).values(
                'thumbnail_id__url'
            ).first()[
                'thumbnail_id__url'
            ]
        )

        self.assertTrue(
            res.json()[
                'range_list'
            ]
        )


    def test_paginate_req_contents_length(self):

        # if front request with query string
        a, b, c = clnt.get(
            '/music/main'
        ).json()[
            'range_list'
        ][:3]

        self.assertEqual(
            len(
                clnt.get(
                    f'/music/main?collection_id={a}&collection_id={b}&collection_id={c}'
                ).json()[
                    'contents'
                ]
            ),
            3
        )

    def test_paginate_req_unexpected_keys(self):

        # if front request with query string
        a, b, c = clnt.get(
            '/music/main'
        ).json()[
            'range_list'
        ][:3]

        res = clnt.get(
            f'/music/main?collection_id={a}&collection_id={b}&collction_id={c}'
        )

    def test_get_404(self):
        client = Client()
        response = client.get('/muzic/')
        def for_test():

            try:

                res.json()[
                    'main_thumb'
                ]

                res.json()[
                    'range_list'
                ]

                return True

            except KeyError:

                return False

        self.assertFalse(for_test())


class ListViewTest(TestCase):

    def test_(self):

        assert

            {
                'list_meta':playlist.annotate(
                    list_name   = F('name'),
                    list_desc   = F('description'),
                    list_artist = F('artist'),
                    list_year   = F('year'),
                    list_thumb  = F('thumbnail_id__url'),
                    list_type   = F('type_id__name')
                ).values(
                    'list_name',
                    'list_desc',
                    'list_artist',
                    'list_year',
                    'list_thumb',
                    'list_type'
                ).first(),
                'elements':list(
                    playlist.annotate(
                        item_id     = F('media__id'),
                        item_thumb  = F('media__thumbnail_id__url'),
                        item_name   = F('media__name'),
                        item_artist = F('media__artist_id__name'),
                        item_album  = F('media__album'),
                        item_length = F('media__length'),
                    ).values(
                        'item_id',
                        'item_thumb',
                        'item_name',
                        'item_artist',
                        'item_album',
                        'item_length',
                    )
                )
            }
