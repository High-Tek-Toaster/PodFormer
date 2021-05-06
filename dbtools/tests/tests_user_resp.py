from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from dbtools.models import *


def create_sample_groupformer():
    gfs = {}
    gfs[1] = {}
    gfs[1]['gf'] = GroupFormer.objects.create(prof_name="Min Chon", prof_email="minc1@umbc.edu", class_section="34")
    gfs[2] = {}
    gfs[2]['gf'] = GroupFormer.objects.create(prof_name="Ben Johnson", prof_email="ben.johnson@umbc.edu",
                                              class_section="24")
    return gfs


def create_sample_projects(gfs):
    gfs[1]['p1'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Groupformer Tool",
                                          project_description="Create a tool that creates groups!")
    gfs[1]['p2'] = Project.objects.create(group_former=gfs[1]['gf'], project_name="Robot that pees beer",
                                          project_description="Create a modification on a very expensive robot dog!")

    gfs[2]['p1'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="Literally Something",
                                          project_description="Literally Anything!")
    gfs[2]['p2'] = Project.objects.create(group_former=gfs[2]['gf'], project_name="What",
                                          project_description="I dont know.")


def create_sample_attributes(gfs):
    # Intentionally do not create attributes for second groupformer
    gfs[1]['a1'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Back-End", is_homogenous=False,
                                            is_continuous=True)
    gfs[1]['a2'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Front-End", is_homogenous=True,
                                            is_continuous=True)
    gfs[1]['a3'] = Attribute.objects.create(group_former=gfs[1]['gf'], attr_name="Dog Lover", is_homogenous=False,
                                            is_continuous=False)


def create_sample_participants(gfs):
    names = ["Min", "Kristian", "Sarah", "Morgan", "Kyle", "Ben", "Eric", "Andrew"]
    for i in range(len(names)):
        gfs[1]['part' + str(i + 1)] = Participant.objects.create(group_former=gfs[1]['gf'], part_name=names[i],
                                                                 part_email=f"{names[i]}@email.com")
        gfs[2]['part' + str(i + 1)] = Participant.objects.create(group_former=gfs[2]['gf'], part_name=names[i],
                                                                 part_email=f"{names[i]}@email.com")
    return names


def create_all_samples():
    gfs = create_sample_groupformer()
    create_sample_projects(gfs)
    create_sample_attributes(gfs)
    create_sample_participants(gfs)
    return gfs

class SeleniumResponseScreen(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(1)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login_to_sample_groupformer(self, groupformer_id):
        self.selenium.get(
            self.live_server_url + reverse('response_screen:login', kwargs={'groupformer_id': groupformer_id}))

        self.selenium.find_element_by_id('email').send_keys("Kristian@email.com")
        self.selenium.find_element_by_id('login-submit').click()

        # Should be redirected to response screen
        self.assertTrue(self.selenium.current_url.endswith(f"/response_screen/{groupformer_id}"))

    def test_fill_response_screen(self):
        """
        Test that users are required to input important fields such as Name, Email, and all preference boxes
        """
        gfs = create_all_samples()
        # ID is necessary because each Selenium test does not create its own isolated DB for models
        gfs1 = gfs[1]['gf'].id
        gfs2 = gfs[2]['gf'].id

        self.login_to_sample_groupformer(gfs1)
        #########################################
        # Test for the first groupformer object #
        #########################################
        self.selenium.get(
            self.live_server_url + reverse('response_screen:response_screen', kwargs={'groupformer_id': gfs1}))
        # Select preferences for both projects
        self.selenium.find_element_by_xpath(
            "//select[@id='projForm{}']/option[text()='Very Interested']".format(gfs[1]['p1'].pk)).click()
        self.selenium.find_element_by_xpath(
            "//select[@id='projForm{}']/option[text()='PLEASE NO']".format(gfs[1]['p2'].pk)).click()
        # Select preferences for all attributes
        self.selenium.find_element_by_xpath(
            "//select[@id='attrForm{}']/option[text()='4']".format(gfs[1]['a1'].pk)).click()
        self.selenium.find_element_by_xpath(
            "//select[@id='attrForm{}']/option[text()='2']".format(gfs[1]['a2'].pk)).click()
        self.selenium.find_element_by_xpath(
            "//select[@id='attrForm{}']/option[text()='5 (Most preferred)']".format(gfs[1]['a3'].pk)).click()
        # Select a few students
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Kristian']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Min']").click()
        self.selenium.find_element_by_xpath("//select[@id='participantForm']/option[text()='Ben']").click()
        # Submit
        self.selenium.find_element_by_xpath("//button[@id='submitForm']").click()



        # For each attribute form, the homogenous/continuous values are a hidden form retrieved from the model.
        # Check if those attributes carried over the correct values for those model objects.

        self.assertEqual(len(project_selection.objects.all()), 2)
        self.assertEqual(len(attribute_selection.objects.all()), 3)

        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p1']).value, 5)
        self.assertEqual(gfs[1]['part2'].getProjectChoice(gfs[1]['p2']).value, 1)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a1']).value, 4)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a2']).value, 2)
        self.assertEqual(gfs[1]['part2'].getAttributeChoice(gfs[1]['a3']).value, 5)
        self.assertSetEqual({'Min', 'Kristian', 'Ben'}, {x.part_name for x in gfs[1]['part2'].desired_partner.all()})





